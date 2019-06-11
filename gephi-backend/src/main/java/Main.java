import com.opencsv.CSVReader;
import com.opencsv.CSVReaderHeaderAware;
import org.gephi.appearance.api.AppearanceController;
import org.gephi.appearance.api.AppearanceModel;
import org.gephi.appearance.api.Function;
import org.gephi.appearance.plugin.RankingElementColorTransformer;
import org.gephi.appearance.plugin.RankingNodeSizeTransformer;
import org.gephi.graph.api.*;
import org.gephi.io.exporter.api.ExportController;
import org.gephi.io.exporter.plugin.ExporterCSV;
import org.gephi.io.generator.plugin.RandomGraph;
import org.gephi.io.importer.api.Container;
import org.gephi.io.importer.api.ImportController;
import org.gephi.io.processor.plugin.DefaultProcessor;
import org.gephi.layout.plugin.AutoLayout;
import org.gephi.layout.plugin.forceAtlas.ForceAtlasLayout;
import org.gephi.preview.api.PreviewController;
import org.gephi.preview.api.PreviewModel;
import org.gephi.preview.api.PreviewProperties;
import org.gephi.preview.api.PreviewProperty;
import org.gephi.preview.types.DependantColor;
import org.gephi.preview.types.DependantOriginalColor;
import org.gephi.project.api.ProjectController;
import org.gephi.project.api.Workspace;
import org.gephi.statistics.plugin.GraphDistance;
import org.openide.util.Lookup;

import java.awt.*;
import java.io.*;
import java.util.Arrays;
import java.util.Map;
import java.util.Scanner;
import java.util.concurrent.TimeUnit;


public class Main {

    public static void main(String[] args) {
        //Init a project - and therefore a workspace
        ProjectController pc = Lookup.getDefault().lookup(ProjectController.class);
        pc.newProject();
        Workspace workspace = pc.getCurrentWorkspace();

        // Read graph from the standard input into a container
        Container container = Lookup.getDefault().lookup(Container.Factory.class).newContainer();
        GraphModel graphModel = Lookup.getDefault().lookup(GraphController.class).getGraphModel();
        GraphFactory graphFactory = graphModel.factory();
        UndirectedGraph undirectedGraph = graphModel.getUndirectedGraph();

        // Read all the input
        StringBuilder nodesStringBuilder = new StringBuilder();
        StringBuilder edgesStringBuilder = new StringBuilder();
        Scanner scanner = new Scanner(System.in);

        StringBuilder builder = nodesStringBuilder;
        while (scanner.hasNextLine()) {
            String line = scanner.nextLine();
            if (line.equals("")) {
                builder = edgesStringBuilder;
                continue;
            }
            builder.append(line + "\n");

        }

        String nodesString = nodesStringBuilder.toString();
        String edgesString = edgesStringBuilder.toString();

        CSVReaderHeaderAware csvReader;
        Map<String, String> nextRecord;

        // NODES
        Table nodeTable = graphModel.getNodeTable();
        nodeTable.addColumn("external_id", String.class);
        nodeTable.addColumn("description", String.class);

        Color proteinColor = new Color(70, 170, 220);

        try  {
            StringReader stringReader = new StringReader(nodesString);
            csvReader = new CSVReaderHeaderAware(stringReader);
            while (true) {
                String[] tokens = csvReader.peek();
                if (tokens == null || tokens.length == 1 && tokens[0].equals("")) {
                    break;
                }

                nextRecord = csvReader.readMap();

                String id = nextRecord.get("id");
                String external_id = nextRecord.get("external_id");
                String name = nextRecord.get("name");
                String description = nextRecord.get("description");

                Node n = graphFactory.newNode(id);
                n.setLabel(name);
                n.setAttribute("external_id", external_id);
                n.setAttribute("description", description);
                n.setColor(proteinColor);
                n.setSize(5);

                undirectedGraph.addNode(n);
            }
        }
        catch (IOException ex) {
            ex.printStackTrace();
        }
        System.err.println("Nodes:" + undirectedGraph.getNodeCount());

        // EDGES
        Table edgeTable = graphModel.getEdgeTable();
        edgeTable.addColumn("score", Integer.class);

        try {
            StringReader stringReader = new StringReader(edgesString);
            csvReader = new CSVReaderHeaderAware(stringReader);

            while (true) {
                String[] tokens = csvReader.peek();
                if (tokens == null || tokens.length == 1 && tokens[0].equals("")) {
                    break;
                }

                nextRecord = csvReader.readMap();

                String source = nextRecord.get("source");
                String target = nextRecord.get("target");
                String score = nextRecord.get("score");

                Node n1 = undirectedGraph.getNode(source);
                Node n2 = undirectedGraph.getNode(target);
                Edge e = graphFactory.newEdge(n1, n2, false);
                e.setAttribute("score",  Integer.parseInt(score));

                undirectedGraph.addEdge(e);
            }
        } catch (IOException ex) {
            ex.printStackTrace();
        }
        System.err.println("Edges:" + undirectedGraph.getEdgeCount());

        // Append container to graph structure
        ImportController importController = Lookup.getDefault().lookup(ImportController.class);
        importController.process(container, new DefaultProcessor(), workspace);

        // Style
        PreviewController previewController = Lookup.getDefault().lookup(PreviewController.class);
        PreviewModel previewModel = previewController.getModel();
        PreviewProperties previewProperties = previewModel.getProperties();
        previewProperties.putValue(PreviewProperty.EDGE_CURVED, Boolean.FALSE);
        previewProperties.putValue(PreviewProperty.EDGE_OPACITY, 50);
        previewProperties.putValue(PreviewProperty.NODE_BORDER_WIDTH, 0);

        //
        AppearanceController appearanceController = Lookup.getDefault().lookup(AppearanceController.class);
        AppearanceModel appearanceModel = appearanceController.getModel();

        //Rank color by Degree
        Function degreeRanking = appearanceModel.getNodeFunction(undirectedGraph, AppearanceModel.GraphFunction.NODE_DEGREE, RankingElementColorTransformer.class);
        RankingElementColorTransformer degreeTransformer = (RankingElementColorTransformer) degreeRanking.getTransformer();
        degreeTransformer.setColors(new Color[]{new Color(0x424fff), new Color(0x42fffa), new Color(0x42ff46), new Color(0xf4ff42), new Color(0xff4242)});
        degreeTransformer.setColorPositions(new float[]{0f, 1f});
        appearanceController.transform(degreeRanking);

        //Get Centrality
        GraphDistance distance = new GraphDistance();
        distance.setNormalized(true);
        distance.execute(graphModel);

        //Rank size by centrality
        Column centralityColumn = graphModel.getNodeTable().getColumn(GraphDistance.BETWEENNESS);
        Function centralityRanking = appearanceModel.getNodeFunction(undirectedGraph, centralityColumn, RankingNodeSizeTransformer.class);
        RankingNodeSizeTransformer centralityTransformer = (RankingNodeSizeTransformer) centralityRanking.getTransformer();
        centralityTransformer.setMinSize(5);
        centralityTransformer.setMaxSize(20);
        appearanceController.transform(centralityRanking);

        // TODO Color edges by score
        Column scoreColumn = edgeTable.getColumn("score");
        Function scoreRanking = appearanceModel.getEdgeFunction(undirectedGraph, scoreColumn, RankingElementColorTransformer.class);

        RankingElementColorTransformer edgeColorTransformer = scoreRanking.getTransformer();
        edgeColorTransformer.setColors(new Color[]{new Color(0x424fff), new Color(0x42fffa), new Color(0x42ff46), new Color(0xf4ff42), new Color(0xff4242)});
        edgeColorTransformer.setColorPositions(new float[]{0f, 1f});
        appearanceController.transform(scoreRanking);

        // Layout
        AutoLayout autoLayout = new AutoLayout(60, TimeUnit.SECONDS);
        autoLayout.setGraphModel(graphModel);

        // Force Atlas layout
        ForceAtlasLayout secondLayout = new ForceAtlasLayout(null);
        AutoLayout.DynamicProperty repulsionProperty = AutoLayout.createDynamicProperty("forceAtlas.repulsionStrength.name", 500., 0f);//500 for the complete period
        autoLayout.addLayout(secondLayout, 1.f, new AutoLayout.DynamicProperty[]{repulsionProperty});
        autoLayout.execute();

        ExportController ec = Lookup.getDefault().lookup(ExportController.class);
        try {
            ec.exportFile(new File("out.png"));
        } catch (IOException e) {
            e.printStackTrace();
        }

//        // Print to the standard output as CSV
//
//        ExporterCSV exporterCSV = (ExporterCSV) ec.getExporter("csv");
//        exporterCSV.setExportVisible(true);
//        exporterCSV.setWorkspace(workspace);
//
//        StringWriter writer = new StringWriter();
//
//        ec.exportWriter(writer, exporterCSV);
//        System.out.print(writer.toString());
    }


}

import com.opencsv.CSVReaderHeaderAware;
import jsonexporter.JSONExporter;
import org.gephi.appearance.api.*;
import org.gephi.appearance.plugin.PartitionElementColorTransformer;
import org.gephi.appearance.plugin.RankingNodeSizeTransformer;
import org.gephi.appearance.plugin.palette.Palette;
import org.gephi.appearance.plugin.palette.PaletteManager;
import org.gephi.graph.api.*;
import org.gephi.io.exporter.api.ExportController;
import org.gephi.layout.plugin.AutoLayout;
import org.gephi.layout.plugin.forceAtlas2.ForceAtlas2;
import org.gephi.preview.api.*;
import org.gephi.preview.types.EdgeColor;
import org.gephi.project.api.ProjectController;
import org.gephi.project.api.Workspace;
import org.gephi.statistics.plugin.GraphDistance;
import org.gephi.statistics.plugin.Modularity;
import org.javatuples.Pair;
import org.openide.util.Lookup;

import java.awt.*;
import java.io.*;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Scanner;
import java.util.concurrent.TimeUnit;


public class Main {

    public static void main(String[] args) {

        // Init a project - and therefore a workspace
        ProjectController pc = Lookup.getDefault().lookup(ProjectController.class);
        pc.newProject();
        Workspace workspace = pc.getCurrentWorkspace();
        GraphModel graphModel = Lookup.getDefault().lookup(GraphController.class).getGraphModel();
        UndirectedGraph undirectedGraph = graphModel.getUndirectedGraph();

        // Read nodes and edges tables from the standard input
        Pair<String, String> tablesStringPair = readInput();
        String nodesString = tablesStringPair.getValue0();
        String edgesString = tablesStringPair.getValue1();

        // Edges
        List<Node> nodes = parseNodes(nodesString, graphModel);
        for (Node n : nodes)
            undirectedGraph.addNode(n);
        System.err.println("Nodes:" + undirectedGraph.getNodeCount());

        // Edges
        List<Edge> edges = parseEdges(edgesString, graphModel);
        for (Edge e : edges)
            undirectedGraph.addEdge(e);
        System.err.println("Edges:" + undirectedGraph.getEdgeCount());


        // Appearance controller
        AppearanceController appearanceController = Lookup.getDefault().lookup(AppearanceController.class);

        // Style
        setPreviewProperties();

        // Rank node size by centrality
        rankNodeSizeByCentrality(graphModel, appearanceController);

        // Partition node color by modularity
        partitionNodeColorByModularity(graphModel, appearanceController);

        // Layout
        runLayout(graphModel);

        // Set edge colors (mixture between source and target color)
        setEdgeColors(undirectedGraph);

        // Write to standard output
        outputJson(graphModel, workspace);

        // Stupid hack, otherwise the program doesn't terminate (probably some Gephi thread/process in the background)
        System.exit(0);
    }

    private static void setEdgeColors(Graph graph) {
        int alpha = 50;
        for (Edge e : graph.getEdges()) {
            Color sourceColor = e.getSource().getColor();
            Color targetColor = e.getTarget().getColor();

            int r = (sourceColor.getRed() + targetColor.getRed()) / 2;
            int g = (sourceColor.getGreen() + targetColor.getGreen()) / 2;
            int b = (sourceColor.getBlue() + targetColor.getBlue()) / 2;

            e.setColor(new Color(r, g, b, alpha));
        }
    }

    private static Pair<String, String> readInput() {
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
        return new Pair<String, String>(nodesString, edgesString);
    }

    private static List<Node> parseNodes(String nodesString, GraphModel graphModel) {
        ArrayList<Node> nodes = new ArrayList<Node>();

        Table nodeTable = graphModel.getNodeTable();
        // nodeTable.addColumn("external_id", String.class);
        // nodeTable.addColumn("description", String.class);

        GraphFactory graphFactory = graphModel.factory();

        CSVReaderHeaderAware csvReader;
        Map<String, String> nextRecord;

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
                // String external_id = nextRecord.get("external_id");
                // String name = nextRecord.get("name");
                // String description = nextRecord.get("description");

                Node n = graphFactory.newNode(id);
                // n.setLabel(name);
                // n.setAttribute("external_id", external_id);
                // n.setAttribute("description", description);
                nodes.add(n);
            }
            csvReader.close();
            stringReader.close();
        }
        catch (IOException ex) {
            ex.printStackTrace();
        }

        return nodes;
    }

    private static List<Edge> parseEdges(String edgesString, GraphModel graphModel) {
        ArrayList<Edge> edges = new ArrayList<Edge>();

        Table edgeTable = graphModel.getEdgeTable();
        edgeTable.addColumn("score", Integer.class);

        GraphFactory graphFactory = graphModel.factory();
        UndirectedGraph undirectedGraph = graphModel.getUndirectedGraph();

        CSVReaderHeaderAware csvReader;
        Map<String, String> nextRecord;

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
                if (n1 == null || n2 == null)
                    continue;

                Edge e = graphFactory.newEdge(n1, n2, false);
                e.setAttribute("score",  Integer.parseInt(score));

                edges.add(e);
            }

            csvReader.close();
            stringReader.close();
        } catch (IOException ex) {
            ex.printStackTrace();
        }

        return edges;
    }

    private static void setPreviewProperties() {
        PreviewController previewController = Lookup.getDefault().lookup(PreviewController.class);
        PreviewModel previewModel = previewController.getModel();
        PreviewProperties previewProperties = previewModel.getProperties();
        previewProperties.putValue(PreviewProperty.EDGE_CURVED, Boolean.FALSE);
        previewProperties.putValue(PreviewProperty.EDGE_OPACITY, 50);
        previewProperties.putValue(PreviewProperty.NODE_BORDER_WIDTH, 0);
        previewProperties.putValue(PreviewProperty.EDGE_COLOR, EdgeColor.Mode.MIXED);
    }

    private static void rankNodeSizeByCentrality(GraphModel graphModel, AppearanceController appearanceController) {
        AppearanceModel appearanceModel = appearanceController.getModel();
        UndirectedGraph undirectedGraph = graphModel.getUndirectedGraph();

        // Graph distance
        GraphDistance distance = new GraphDistance();
        distance.setNormalized(true);
        distance.execute(graphModel);

        // Ranking
        Column centralityColumn = graphModel.getNodeTable().getColumn(GraphDistance.BETWEENNESS);
        Function centralityRanking = appearanceModel.getNodeFunction(undirectedGraph, centralityColumn, RankingNodeSizeTransformer.class);
        RankingNodeSizeTransformer centralityTransformer = centralityRanking.getTransformer();
        centralityTransformer.setMinSize(5);
        centralityTransformer.setMaxSize(20);
        appearanceController.transform(centralityRanking);
    }

    private static void partitionNodeColorByModularity(GraphModel graphModel, AppearanceController appearanceController) {
        AppearanceModel appearanceModel = appearanceController.getModel();
        UndirectedGraph undirectedGraph = graphModel.getUndirectedGraph();

        Modularity modularity = new Modularity();
        modularity.setUseWeight(true);
        modularity.setRandom(true);
        modularity.execute(graphModel);

        Column modularityColumn = graphModel.getNodeTable().getColumn(Modularity.MODULARITY_CLASS);
        Function modularityPartitioning = appearanceModel.getNodeFunction(undirectedGraph, modularityColumn, PartitionElementColorTransformer.class);
        Partition partition = ((PartitionFunction) modularityPartitioning).getPartition();

        PaletteManager paletteManager = PaletteManager.getInstance();
        Palette randomPalette = paletteManager.generatePalette(partition.size());
        partition.setColors(randomPalette.getColors());

        appearanceController.transform(modularityPartitioning);
    }

    private static void runLayout(GraphModel graphModel) {
        AutoLayout autoLayout = new AutoLayout(1, TimeUnit.SECONDS);
        autoLayout.setGraphModel(graphModel);

        // ForceAtlas2 layout
        ForceAtlas2 forceAtlas2 = new ForceAtlas2(null);
        forceAtlas2.setScalingRatio(500.); // Repulsion
        autoLayout.addLayout(forceAtlas2, 1.f);
        autoLayout.execute();
    }


    private static void outputJson(GraphModel graphModel, Workspace workspace) {
        for (Edge e: graphModel.getUndirectedGraph().getEdges()) {
            e.setWeight(0.05);
        }

        OutputStreamWriter writer = new OutputStreamWriter(System.out);

        JSONExporter jsonExporter = new JSONExporter();
        jsonExporter.setExportVisible(true);
        jsonExporter.setWorkspace(workspace);
        jsonExporter.setWriter(writer);
        jsonExporter.execute(); // Hacked implementation that writes to standard output
    }





}

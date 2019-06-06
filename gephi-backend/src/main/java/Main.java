import com.opencsv.CSVReader;
import com.opencsv.CSVReaderHeaderAware;
import org.gephi.graph.api.*;
import org.gephi.io.exporter.api.ExportController;
import org.gephi.io.exporter.plugin.ExporterCSV;
import org.gephi.io.generator.plugin.RandomGraph;
import org.gephi.io.importer.api.Container;
import org.gephi.io.importer.api.ImportController;
import org.gephi.io.processor.plugin.DefaultProcessor;
import org.gephi.layout.plugin.AutoLayout;
import org.gephi.layout.plugin.forceAtlas.ForceAtlasLayout;
import org.gephi.project.api.ProjectController;
import org.gephi.project.api.Workspace;
import org.openide.util.Lookup;

import java.io.*;
import java.util.Map;


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

        InputStreamReader stdinReader = new InputStreamReader(System.in);
        CSVReaderHeaderAware csvReader;
        Map<String, String> nextRecord;

        // NODES
        Table nodeTable = graphModel.getNodeTable();
        nodeTable.addColumn("external_id", String.class);
        nodeTable.addColumn("description", String.class);

        try  {
            csvReader = new CSVReaderHeaderAware(stdinReader);
            while ((nextRecord = csvReader.readMap()) != null) {
                String id = nextRecord.get("id");
                String external_id = nextRecord.get("external_id");
                String name = nextRecord.get("name");
                String description = nextRecord.get("description");

                Node n = graphFactory.newNode(id);
                n.setLabel(name);
                n.setAttribute("external_id", external_id);
                n.setAttribute("description", description);

                undirectedGraph.addNode(n);

                System.out.println(nextRecord);
            }
        }
        catch (IOException ex) {}
        System.err.println("Nodes:" + undirectedGraph.getNodeCount());

        // EDGES
        Table edgeTable = graphModel.getEdgeTable();
        edgeTable.addColumn("score", Integer.class);

        try {
            csvReader = new CSVReaderHeaderAware(stdinReader);
            // Edges
            while ((nextRecord = csvReader.readMap()) != null) {
                String source = nextRecord.get("source");
                String target = nextRecord.get("target");
                String score = nextRecord.get("score");

                Node n1 = undirectedGraph.getNode(source);
                Node n2 = undirectedGraph.getNode(target);
                Edge e = graphFactory.newEdge(n1, n2, false);
                e.setAttribute("score", Integer.getInteger(score));

                undirectedGraph.addEdge(e);

                System.out.println(nextRecord);
            }
        }
        catch (IOException ex) {}
        System.err.println("Edges:" + undirectedGraph.getEdgeCount());

//        // Append container to graph structure
//        ImportController importController = Lookup.getDefault().lookup(ImportController.class);
//        importController.process(container, new DefaultProcessor(), workspace);
//
//        // See if graph is well imported
//        DirectedGraph graph = graphModel.getDirectedGraph();
//        System.out.println("Nodes: " + graph.getNodeCount());
//        System.out.println("Edges: " + graph.getEdgeCount());
//
//        // Layout for 1 minute
//        AutoLayout autoLayout = new AutoLayout(1, TimeUnit.MINUTES);
//        autoLayout.setGraphModel(graphModel);
//
//        // Force Atlas layout
//        ForceAtlasLayout secondLayout = new ForceAtlasLayout(null);
//        AutoLayout.DynamicProperty adjustBySizeProperty = AutoLayout.createDynamicProperty("forceAtlas.adjustSizes.name", Boolean.TRUE, 0.1f);//True after 10% of layout time
//        AutoLayout.DynamicProperty repulsionProperty = AutoLayout.createDynamicProperty("forceAtlas.repulsionStrength.name", 500., 0f);//500 for the complete period
//        autoLayout.addLayout(secondLayout, 1.f, new AutoLayout.DynamicProperty[]{adjustBySizeProperty, repulsionProperty});
//
//        autoLayout.execute();
//
//        // Print to the standard output as CSV
//        ExportController ec = Lookup.getDefault().lookup(ExportController.class);
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

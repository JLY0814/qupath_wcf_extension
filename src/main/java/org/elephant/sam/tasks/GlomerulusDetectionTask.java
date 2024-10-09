package org.elephant.sam.tasks;

import qupath.lib.gui.QuPathGUI;
import javafx.concurrent.Task;
import java.io.IOException;
import org.elephant.sam.parameters.GlomerulusDetectionParameters;


public class GlomerulusDetectionTask extends Task<Void> {
    private final QuPathGUI qupath;
    private final String modelDir;
    private final String demoDir;
    private final String targetDir;

    public GlomerulusDetectionTask(QuPathGUI qupath, GlomerulusDetectionParameters parameters) {
        this.qupath = qupath;
        this.modelDir = parameters.getModelDir();
        this.demoDir = parameters.getDemoDir();
        this.targetDir = parameters.getTargetDir();
    }

    @Override
    protected Void call() throws Exception {
        String command = buildCommand();
        ProcessBuilder processBuilder = new ProcessBuilder(command.split(" "));
        processBuilder.redirectErrorStream(true);

        try {
            Process process = processBuilder.start();
            int exitCode = process.waitFor(); // Wait for the process to finish
            if (exitCode != 0) {
                updateMessage("Error executing Python script");
            }
        } catch (IOException e) {
            updateMessage("Failed to start the process: " + e.getMessage());
        }

        return null;
    }

    private String buildCommand() {
        return String.format("python3 WCF/run_detection_for_scn.py circledet --circle_fusion --generate_geojson --load_model_dir \"%s\" --demo \"%s\" --target_dir \"%s\"",
                modelDir, demoDir, targetDir);
    }
}


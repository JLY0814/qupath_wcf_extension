package org.elephant.sam;

import qupath.lib.gui.extensions.GitHubProject;
import qupath.lib.gui.extensions.QuPathExtension;
import qupath.lib.gui.QuPathGUI;
import javafx.application.Platform;

public class GlomerulusDetectionExtension implements QuPathExtension, GitHubProject {

    public String getDescription() {
        return "Detect glomeruli in whole slide images.";
    }

    public String getName() {
        return "Glo Detection";
    }

    public void installExtension(QuPathGUI qupath) {
        qupath.installActions(new GloDetectionCommand(qupath));
    }

    private class GloDetectionCommand {

        private final QuPathGUI qupath;

        public GloDetectionCommand(QuPathGUI qupath) {
            this.qupath = qupath;
        }

        public void run() {
            String wsiPath = getCurrentImagePath();
            if (wsiPath != null) {
                GlomerulusDetectionParameters parameters = GlomerulusDetectionParameters.builder()
                        .modelDir("WCF/model")
                        .demoDir("WCF")
                        .targetDir("WCF/xml_result")
                        .wsiPath(wsiPath)
                        .build();

                GlomerulusDetectionTask task = new GlomerulusDetectionTask(qupath, parameters);
                new Thread(task).start();
            } else {
                // Handle case where no WSI is available
                updateInfoTextWithError("No image available!");
            }
        }

        private String getCurrentImagePath() {
            // Implement logic to get the current WSI path from QuPath
            // Return the path as a String
        }

        private void updateInfoTextWithError(String message) {
            // Implement logic to update the user with an error message
        }
    }

    @Override
    public GitHubRepo getRepository() {
        return GitHubRepo.create(getName(), "yourusername", "your-repo-name");
    }

    @Override
    public Version getQuPathVersion() {
        return Version.parse("0.7.0");
    }
}

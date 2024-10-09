package org.elephant.sam.parameters;

import java.util.Objects;

public class GlomerulusDetectionParameters {

    private String command = "python3 WCF/run_detection_for_scn.py";
    private String modelDir;
    private String demoDir;
    private String targetDir;
    private String wsiPath; // 添加 WSI 路径

    private GlomerulusDetectionParameters(final Builder builder) {
        this.modelDir = builder.modelDir;
        this.demoDir = builder.demoDir;
        this.targetDir = builder.targetDir;
        this.wsiPath = builder.wsiPath; // 初始化 WSI 路径

        Objects.requireNonNull(modelDir, "Model directory must be specified");
        Objects.requireNonNull(demoDir, "Demo directory must be specified");
        Objects.requireNonNull(targetDir, "Target directory must be specified");
        Objects.requireNonNull(wsiPath, "WSI path must be specified"); // 确保 WSI 路径不为空
    }

    public static Builder builder() {
        return new Builder();
    }

    public String buildCommand() {
        return String.format("%s circledet --circle_fusion --generate_geojson --arch dla_34 --load_model_dir \"WCF/model\" --demo \"%s\" --target_dir \"WCF/xml_result\"",
                command, wsiPath); // 使用 WSI 路径
    }

    public static class Builder {
        private String modelDir;
        private String demoDir;
        private String targetDir;
        private String wsiPath; // 添加 WSI 路径

        public Builder modelDir(String modelDir) {
            this.modelDir = modelDir;
            return this;
        }

        public Builder demoDir(String demoDir) {
            this.demoDir = demoDir;
            return this;
        }

        public Builder targetDir(String targetDir) {
            this.targetDir = targetDir;
            return this;
        }

        public Builder wsiPath(String wsiPath) { // 设置 WSI 路径的方法
            this.wsiPath = wsiPath;
            return this;
        }

        public GlomerulusDetectionParameters build() {
            return new GlomerulusDetectionParameters(this);
        }
    }
}


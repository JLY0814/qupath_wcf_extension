package org.elephant.sam.commands;

import java.awt.image.BufferedImage;
import javafx.application.Platform;
import javafx.beans.property.StringProperty;
import qupath.lib.gui.QuPathGUI;
import qupath.lib.images.ImageData;
import qupath.lib.viewer.QuPathViewer;

public class SAMMainCommand implements Runnable {

    private final QuPathGUI qupath;

    public SAMMainCommand(QuPathGUI qupath) {
        this.qupath = qupath;
    }

    @Override
    public void run() {
        showStage();
    }

    private String getCurrentImagePath() {
        QuPathViewer viewer = qupath.getViewer();
        if (viewer != null) {
            ImageData<BufferedImage> imageData = viewer.getImageData();
            if (imageData != null) {
                return imageData.getServer().getPath(); // 返回图像文件的路径
            }
        }
        return null; // 如果没有图像，返回 null
    }

    public void runAutoMask() {
        String wsiPath = getCurrentImagePath();
        if (wsiPath == null) {
            updateInfoTextWithError("No image available!");
            return;
        }
        // 此处继续执行自动掩膜逻辑，并使用 wsiPath
    }

    private void updateInfoTextWithError(String message) {
        // 更新错误信息文本
    }

    private void showStage() {
        // 显示窗口逻辑
    }
}

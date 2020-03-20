#include "StudentPreProcessing.h"


IntensityImage * StudentPreProcessing::stepToIntensityImage(const RGBImage &image) const {
	return nullptr;
}

IntensityImage * StudentPreProcessing::stepScaleImage(const IntensityImage &image) const {
	return nullptr;
}

IntensityImage * StudentPreProcessing::stepEdgeDetection(const IntensityImage &image) const {
	//-2 on both width and heigth because of kernel
	const int size = 9;
	IntensityImage * newImage = new IntensityImagePrivate(image.getWidth() - size + 1, image.getHeight() - size + 1);
	const auto basicKernel = basicKernels::SobelY;
	const auto kernel = Kernel<size>(basicKernel);
	kernel.apply(image, newImage, false);
	return newImage;
}

IntensityImage * StudentPreProcessing::stepThresholding(const IntensityImage &image) const {
	const uint8_t Threshold = 30;
	IntensityImage* newImage = new IntensityImagePrivate(image.getWidth(), image.getHeight());
	for (int i = 0; i < image.getWidth(); i++) {
		for (int j = 0; j < image.getHeight(); j++) {
			if (image.getPixel(i, j) < Threshold) {
				newImage->setPixel(i, j, 255);
			}
			else {
				newImage->setPixel(i, j, 0);
			}
		}
	}
	return newImage;
}
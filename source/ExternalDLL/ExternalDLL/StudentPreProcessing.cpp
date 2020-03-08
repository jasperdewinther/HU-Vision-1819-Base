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
	const auto basicKernel = basicKernels::Laplace;
	const auto kernel = Kernel<size>(basicKernel);
	kernel.apply(image, newImage);
	return newImage;
}

IntensityImage * StudentPreProcessing::stepThresholding(const IntensityImage &image) const {
	return nullptr;
}
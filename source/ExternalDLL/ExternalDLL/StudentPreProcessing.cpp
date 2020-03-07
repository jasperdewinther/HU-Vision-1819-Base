#include "StudentPreProcessing.h"


IntensityImage * StudentPreProcessing::stepToIntensityImage(const RGBImage &image) const {
	return nullptr;
}

IntensityImage * StudentPreProcessing::stepScaleImage(const IntensityImage &image) const {
	return nullptr;
}

IntensityImage * StudentPreProcessing::stepEdgeDetection(const IntensityImage &image) const {
	//-2 on both width and heigth because of kernel
	IntensityImage * newImage = new IntensityImagePrivate(image.getWidth() - 2, image.getHeight() - 2);
	auto basicKernel = basicKernels::PrewittX;
	auto basicKernel2 = basicKernels::PrewittY;
	auto basicKernel3 = basicKernels::Laplace;
	auto basicKernel4 = basicKernels::LaplaceWithDiagonal;
	auto k1 = Kernel<9>(basicKernel);
	auto k2 = Kernel<15>(basicKernel);
	auto k3 = Kernel<3>(basicKernel);
	auto k4 = Kernel<9>(basicKernel2);
	auto k5 = Kernel<27>(basicKernel3);
	auto k6 = Kernel<3>(basicKernel3);
	auto k7 = Kernel<3>(basicKernel4);
	auto k8 = Kernel<9>(basicKernel4);
	k1.apply(newImage, newImage);
	k2.apply(newImage, newImage);
	k3.apply(newImage, newImage);
	k4.apply(newImage, newImage);
	k5.apply(newImage, newImage);
	k6.apply(newImage, newImage);
	k7.apply(newImage, newImage);
	k8.apply(newImage, newImage);


	return newImage;
}

IntensityImage * StudentPreProcessing::stepThresholding(const IntensityImage &image) const {
	return nullptr;
}
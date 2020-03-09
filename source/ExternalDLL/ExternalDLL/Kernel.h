#pragma once
#include "IntensityImage.h"
#include <stdexcept>
#include <array>
#include <numeric>
#include <iterator>
#include <iostream>
#include <cmath>

namespace basicKernels{
	const std::array<int, 9> SobelX =				{ -1, 0, 1,
													  -2, 0, 2,
													  -1, 0, 1 };
	const std::array<int, 9> SobelY =				{ -1,-2,-1, 
													   0, 0, 0, 
													   1, 2, 1 };
	const std::array<int, 9> Laplace =				{  0,-1, 0,
													  -1, 4,-1, 
													   0,-1, 0 };
	const std::array<int, 9> LaplaceWithDiagonal =	{ -1,-1,-1,
													  -1, 8,-1,
													  -1,-1,-1 };
	const std::array<int, 9> PrewittX =				{ -1, 0, 1,
													  -1, 0, 1,
													  -1, 0, 1 };
	const std::array<int, 9> PrewittY =				{ -1,-1,-1, 
													   0, 0, 0, 
													   1, 1, 1 };
};

//only sizes 3,9,15,21,27 are allowed
template <int size>
class Kernel {
	std::array<int, size*size> m_kernel;
public:
	//construct kernel, and scale to given size
	constexpr Kernel(const std::array<int, 9> & basicKernel) {
		static_assert(size == 3 || size == 9 || size == 15 || size == 21 || size == 27, "Kernel size is not correct");
		for (int i = 0; i < size * size; i++) {
			const int x = static_cast<int>(i / (size / 3)) % 3;
			const int y = i / (size * (size / 3));
			m_kernel[i] = basicKernel[static_cast<int>(x + (y * 3))];
		}
	}


	void apply(const IntensityImage & in, IntensityImage* out) const {
		int startingPointX = static_cast<int>(size / 2);
		int endingPointX = in.getWidth() - static_cast<int>(size / 2) - 1;
		int startingPointY = static_cast<int>(size / 2);
		int endingPointY = in.getHeight() - static_cast<int>(size / 2) - 1;
		for (int i = startingPointX; i < endingPointX; i++) {
			for (int j = startingPointY; j < endingPointY; j++) {
				float kernelResult = 0;
				for (int kernelI = 0; kernelI < size * size; kernelI++) {
					int x = i + (kernelI%size)-static_cast<int>(size/2);
					int y = j + static_cast<int>(kernelI/size) - static_cast<int>(size / 2);
					kernelResult += in.getPixel(x, y) * m_kernel[kernelI];
				}
				if (kernelResult > 255) {
					kernelResult = 255;
				}
				else {
					kernelResult = 0;
				}
				out->setPixel(i - static_cast<int>(size / 2)+1, j - static_cast<int>(size / 2)+1, kernelResult);
			}
		}
	}

	void printKernel() const {
		int counter = 0;
		for (auto& i : m_kernel) {
			if (counter % static_cast<int>(std::sqrt(m_kernel.size())) == 0) {
				std::cout << "\n";
			}
			std::cout << i << " ";
			counter++;
		}
		std::cout << "\n";
	}
};
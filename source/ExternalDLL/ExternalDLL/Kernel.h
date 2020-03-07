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
	Kernel(const std::array<int, 9> & basicKernel) {
		static_assert(size == 3 || size == 9 || size == 15 || size == 21 || size == 27, "Kernel size is not correct");
		if (basicKernel == basicKernels::Laplace || basicKernel == basicKernels::LaplaceWithDiagonal) {

		}
		for (int i = 0; i < size*size; i++) {
			const int x = static_cast<int>(i/(size/3)) % 3;
			const int y = i / (size*(size/3));
			//std::cout << i << " : " << size << " : " << x << " : " << y << " : " << x + (y * 3) << "\n";
			m_kernel[i] = basicKernel[static_cast<int>(x+(y*3))];
		}
		std::cout << "----------\n";
	}


	void apply(IntensityImage* in, IntensityImage* out) const {
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
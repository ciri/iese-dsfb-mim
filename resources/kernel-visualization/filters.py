import numpy as np

class KernelFilters:
    @staticmethod
    def identity():
        """Identity kernel - no change to the image"""
        kernel = np.zeros((5, 5))
        kernel[2, 2] = 1
        return kernel
    
    @staticmethod
    def edge_detection():
        """Standard edge detection (all directions)"""
        return np.array([
            [-1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1],
            [-1, -1, 24, -1, -1],
            [-1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1]
        ])
    
    @staticmethod
    def left_edge():
        """Left edge detection (Sobel X)"""
        return np.array([
            [ 2,  1,  0, -1, -2],
            [ 2,  1,  0, -1, -2],
            [ 4,  2,  0, -2, -4],
            [ 2,  1,  0, -1, -2],
            [ 2,  1,  0, -1, -2]
        ])
    
    @staticmethod
    def right_edge():
        """Right edge detection (Inverted Sobel X)"""
        return np.array([
            [-2, -1,  0,  1,  2],
            [-2, -1,  0,  1,  2],
            [-4, -2,  0,  2,  4],
            [-2, -1,  0,  1,  2],
            [-2, -1,  0,  1,  2]
        ])
    
    @staticmethod
    def top_edge():
        """Top edge detection (Sobel Y)"""
        return np.array([
            [ 2,  2,  4,  2,  2],
            [ 1,  1,  2,  1,  1],
            [ 0,  0,  0,  0,  0],
            [-1, -1, -2, -1, -1],
            [-2, -2, -4, -2, -2]
        ])
    
    @staticmethod
    def bottom_edge():
        """Bottom edge detection (Inverted Sobel Y)"""
        return np.array([
            [-2, -2, -4, -2, -2],
            [-1, -1, -2, -1, -1],
            [ 0,  0,  0,  0,  0],
            [ 1,  1,  2,  1,  1],
            [ 2,  2,  4,  2,  2]
        ])
    
    @staticmethod
    def diagonal_edge():
        """Diagonal edge detection"""
        return np.array([
            [ 4,  3,  2,  1,  0],
            [ 3,  2,  1,  0, -1],
            [ 2,  1,  0, -1, -2],
            [ 1,  0, -1, -2, -3],
            [ 0, -1, -2, -3, -4]
        ])
    
    @staticmethod
    def box_blur():
        """Box blur"""
        return np.array([
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1]
        ])
    
    @staticmethod
    def gaussian_blur():
        """Gaussian blur"""
        return np.array([
            [1, 4, 7, 4, 1],
            [4, 16, 26, 16, 4],
            [7, 26, 41, 26, 7],
            [4, 16, 26, 16, 4],
            [1, 4, 7, 4, 1]
        ])
    
    @staticmethod
    def sharpen():
        """Sharpen"""
        return np.array([
            [ 0,  0, -1,  0,  0],
            [ 0, -1, -1, -1,  0],
            [-1, -1, 13, -1, -1],
            [ 0, -1, -1, -1,  0],
            [ 0,  0, -1,  0,  0]
        ])
    
    @staticmethod
    def emboss():
        """Emboss"""
        return np.array([
            [-2, -2, -1, -1,  0],
            [-2, -1, -1,  0,  1],
            [-1, -1,  1,  1,  1],
            [-1,  0,  1,  1,  2],
            [ 0,  1,  1,  2,  2]
        ])
    
    @staticmethod
    def outline():
        """Outline detection"""
        return np.array([
            [-1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1],
            [-1, -1, 24, -1, -1],
            [-1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1]
        ])
        
    @staticmethod
    def ring_detection():
        return np.array([
            [ 0,  1,  1,  1,  0],
            [ 1, -1, -1, -1,  1],
            [ 1, -1,  8, -1,  1],
            [ 1, -1, -1, -1,  1],
            [ 0,  1,  1,  1,  0]
        ])
    
    @staticmethod
    def motion_blur():
        """Motion blur"""
        return np.array([
            [1, 0, 0, 0, 0],
            [0, 1, 0, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 1, 0],
            [0, 0, 0, 0, 1]
        ])
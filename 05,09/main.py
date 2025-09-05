import numpy as np
import matplotlib.pyplot as plt

# Данные: 2 территории (круги и квадраты), треугольники - случайно
def get_data():
    np.random.seed(42)
    # Круги (класс 0) - красные
    class_circles = np.random.randn(30, 2) + np.array([2, 2])
    y_circles = np.zeros(len(class_circles), dtype=int)
    
    # Квадраты (класс 1) - жёлтые
    class_squares = np.random.randn(30, 2) + np.array([-2, -2])
    y_squares = np.ones(len(class_squares), dtype=int)
    
    # Треугольники - случайные точки в пределах области, без меток (класс 2)
    class_triangles = np.random.uniform(low=-4, high=4, size=(30, 2))
    y_triangles = np.full(len(class_triangles), 2, dtype=int)
    
    X = np.vstack([class_circles, class_squares, class_triangles])
    y = np.concatenate([y_circles, y_squares, y_triangles])
    return X, y

# Класс персептрона "один против всех" для 2 классов (круги и квадраты)
class PerceptronOVR:
    def __init__(self, lr=0.01, n_iter=1000):
        self.lr = lr
        self.n_iter = n_iter
        self.weights = None
        self.bias = None

    def fit(self, X, y):
        n_samples, n_features = X.shape
        # Обучаем только на двух классах: 0 и 1 (круги и квадраты)
        mask = y != 2  # исключаем треугольники из обучения
        X_train = X[mask]
        y_train = y[mask]
        self.classes = np.unique(y_train)
        self.weights = np.zeros((len(self.classes), n_features))
        self.bias = np.zeros(len(self.classes))

        for idx, c in enumerate(self.classes):
            y_binary = np.where(y_train == c, 1, -1)
            w = np.zeros(n_features)
            b = 0
            for _ in range(self.n_iter):
                for xi, target in zip(X_train, y_binary):
                    linear_output = np.dot(xi, w) + b
                    y_pred = 1 if linear_output >= 0 else -1
                    update = self.lr * (target - y_pred)
                    w += update * xi
                    b += update
            self.weights[idx] = w
            self.bias[idx] = b

    def predict(self, X):
        linear_outputs = np.dot(X, self.weights.T) + self.bias
        # Возвращаем -1 для точек вне двух классов (например треугольников) в виде 2
        preds = np.argmax(linear_outputs, axis=1)
        return preds

def plot_territories_and_points(X, y, model):
    # Цвета территорий
    territory_colors = ['red', 'yellow']
    marker_shapes = ['o', 's', '^']  # круг, квадрат, треугольник
    marker_colors = ['red', 'yellow']  # Цвета для кругов и квадратов
    tri_color_default = 'gray'  # Цвет треугольников по умолчанию

    # Создаем сетку для территорий
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.02),
                         np.arange(y_min, y_max, 0.02))
    grid_points = np.c_[xx.ravel(), yy.ravel()]

    # Предсказания для сетки по двум классам (0 и 1)
    Z = model.predict(grid_points)
    Z = Z.reshape(xx.shape)

    # Заливка территорий (только для 2 классов)
    plt.contourf(xx, yy, Z, alpha=0.3, colors=territory_colors)

    # Предсказания для точек (только для 2 классов)
    preds = model.predict(X)

    # Рисуем круги и квадраты с фиксированным цветом
    for cls in [0, 1]:
        cls_points = X[y == cls]
        plt.scatter(cls_points[:, 0], cls_points[:, 1],
                    c=marker_colors[cls],
                    marker=marker_shapes[cls],
                    edgecolor='k', s=100,
                    label=f'Class {"Circle" if cls==0 else "Square"}')

    # Рисуем треугольники, цвет зависит от территории, где оказалась точка
    tri_points = X[y == 2]
    tri_preds = preds[y == 2]  # на какую территорию попали треугольники

    tri_colors = []
    for pred_cls in tri_preds:
        if pred_cls in [0,1]:
            tri_colors.append(territory_colors[pred_cls])
        else:
            tri_colors.append(tri_color_default)

    plt.scatter(tri_points[:, 0], tri_points[:, 1],
                c=tri_colors,
                marker=marker_shapes[2],
                edgecolor='k', s=100,
                label='Triangles')

    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('2 Territories with Circles (red), Squares (yellow), Triangles colored by territory')
    plt.legend()
    plt.show()

def main():
    X, y = get_data()
    perceptron = PerceptronOVR(lr=0.01, n_iter=200)
    perceptron.fit(X, y)
    plot_territories_and_points(X, y, perceptron)

if __name__ == "__main__":
    main()

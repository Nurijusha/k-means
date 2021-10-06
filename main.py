import matplotlib.pyplot as plt
import numpy as np


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f"{self.x} - {self.y}"

    def dist(self, point):
        return np.sqrt((self.x - point.x) ** 2 + (self.y - point.y) ** 2)

    def get_closest_cluster(self, centroids):
        minimum_distance = self.dist(centroids[0])
        minimum = 0
        for i in range(len(centroids)):
            distance = self.dist(centroids[i])
            if minimum_distance > distance:
                minimum_distance = distance
                minimum = i
        return minimum

    @staticmethod
    def get_random_points(length):
        points = []
        for i in range(length):
            point = Point(np.random.randint(0, 100), np.random.randint(0, 100))
            points.append(point)
        return points


class Centroid(Point):
    @staticmethod
    def create_centroids(points, count):
        x = np.mean(list(map(lambda point: point.x, points)))
        y = np.mean(list(map(lambda point: point.y, points)))
        R = 0
        for p in points:
            R = max(R, p.dist(Point(x, y)))
        centroids = []
        for i in range(count):
            point = Centroid(x + R * np.cos(2 * np.pi * i / count), y + R * np.sin(2 * np.pi * i / count))
            centroids.append(point)
        return centroids

    @staticmethod
    def get_centroid(points):
        x = np.mean(list(map(lambda point: point.x, points)))
        y = np.mean(list(map(lambda point: point.y, points)))
        return Centroid(x, y)


class Show:
    @staticmethod
    def results(clusters, centroids):
        for cluster in clusters:
            plt.scatter(list(map(lambda point: point.x, cluster)),
                        list(map(lambda point: point.y, cluster)))

        plt.scatter(list(map(lambda point: point.x, centroids)),
                    list(map(lambda point: point.y, centroids)),
                    color='black')
        plt.show()

    @staticmethod
    def optimal(results, points, k, count):
        criterias = []
        for index in range(len(results) - 1):
            criterias.append(abs(results[index] - results[index + 1])
                             / abs(results[index - 1] - results[index]))

        optimal_index = criterias.index(min(criterias))

        k = optimal_index + 1
        optimal_centroids = Centroid.create_centroids(points, k)
        plt.scatter(list(map(lambda point: point.x, points)),
                    list(map(lambda point: point.y, points)))

        plt.scatter(list(map(lambda point: point.x, optimal_centroids)),
                    list(map(lambda point: point.y, optimal_centroids)),
                    color='black')
        plt.show()

        for i in range(count):
            opt_clustering = []
            for ik in range(k):
                opt_clustering.append([])

            for point in points:
                index = point.get_closest_cluster(optimal_centroids)
                opt_clustering[index].append(point)

            optimal_centroids = []
            for ik in range(k):
                optimal_centroids.append(Centroid.get_centroid(opt_clustering[ik]))

            Show.results(opt_clustering, optimal_centroids)


def get_criteria(clusters, centroids):
    sum = 0
    for i in range(len(clusters)):
        for point in clusters[i]:
            sum += point.dist(centroids[index]) ** 2
    return sum


if __name__ == "__main__":
    n = 2000
    count = 10
    points = Point.get_random_points(n)

    results = []
    cluster_result = []
    centroids_result = []

    for k in range(1, count):
        centroids = Centroid.create_centroids(points, k)

        for c in range(count):
            clusters = [];
            for ik in range(k):
                clusters.append([])

            for point in points:
                index = point.get_closest_cluster(centroids)
                clusters[index].append(point)

            centroid_list = []
            for k1 in range(k):
                centroid_list.append(Centroid.get_centroid(clusters[k1]))

        cluster_result.append(clusters)
        centroids_result.append(centroids)
        results.append(get_criteria(clusters, centroids))

    Show.optimal(results, points, k, count)

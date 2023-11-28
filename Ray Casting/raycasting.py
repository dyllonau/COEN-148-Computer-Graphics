import numpy as np
import matplotlib.pyplot as plt

# Calculates intersection coordinates
def intersection_point(center, radius, ray_origin, ray_direction):
    b = 2*np.dot(ray_direction, ray_origin - center)
    c = np.linalg.norm(ray_origin - center)**2 - radius**2

    if b**2 - 4*c >= 0:
        t1 = (-b + np.sqrt(b**2 - 4*c))/2
        t2 = (-b - np.sqrt(b**2 - 4*c))/2
        if t1 > 0 and t2 > 0: # Takes the first intersected point of vector onto sphere
            return min(t1, t2)
    return None

# Finds the closest object to another as well as the minimum distance between the two among the points
def closest_sphere(spheres, ray_origin, ray_direction):
    distances = [intersection_point(obj['center'], obj['radius'], ray_origin, ray_direction) for obj in spheres]
    closest = None
    min_distance = np.inf
    for i, distance in enumerate(distances):
        if distance and distance < min_distance:
            min_distance = distance
            closest = spheres[i]
    return closest, min_distance

# Normalizes a vector to get unit vectors
def unit_vector(vector): 
    return vector / np.linalg.norm(vector)

width = 200
height = 200

# The light source hitting the spheres
light_source = {'position': np.array([5, 5, 3]), 'color': np.array([1, 1, 1])}

# Three blue spheres
spheres = [
    {'center': np.array([-0.2, 0, -2]), 'radius': 0.7, 'color': np.array([0, 1, 1])},
    {'center': np.array([0, 0.7, 0]), 'radius': 0.2, 'color': np.array([0, 0.5, 0.7])},
    {'center': np.array([-0.3, 0.5, -1]), 'radius': 0.3, 'color': np.array([0, 0.2, 0.4])}]

image = np.zeros((height, width, 3)) # Initializes the viewing plane

# check for intersection of ray from eye across all pixels
for i, y in enumerate(np.linspace(1, -1, height)):
    for j, x in enumerate(np.linspace(-1, 1, width)):
        pixel = np.array([x, y, 0])
        origin = np.array([0, 0, 1])
        direction = unit_vector(pixel - origin)
        color = (0, 0, 0) # Initially set pixel to black
        reflection = 1

        # get intersections of rays with all objects and get the closest one
        closest, min_distance = closest_sphere(spheres, origin, direction)

        # Here, we find if the pixel should be left black, as it would be shaded. This depends on the position of an object over another one and with respect to the light source
        if closest is not None:
            intersection = origin + min_distance * direction
            surface_normal = unit_vector(intersection - closest['center'])

            light_intersection = unit_vector(light_source['position'] - intersection)

            next_closest, min_distance = closest_sphere(spheres, intersection, light_intersection)
            light_intersection_distance = np.linalg.norm(light_source['position'] - intersection)
            shadow = min_distance < light_intersection_distance

            if not shadow:
                
                # refraction and determining the color of the pixel
                refraction = (0, 0, 0)
                refraction += closest['color'] * light_source['color'] * np.dot(light_intersection, surface_normal)
            
                # reflection
                color += reflection * refraction
                reflection *= 0.5
                origin = intersection
                direction - 2*np.dot(direction, surface_normal)*surface_normal

        image[i, j] = np.clip(color, 0, 1) # Displays the pixel

plt.imshow(image)
plt.show()

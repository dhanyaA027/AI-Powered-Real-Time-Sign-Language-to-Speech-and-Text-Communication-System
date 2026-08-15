import numpy as np

def landmarks_to_feature_vector(landmarks):
    pts = np.array([[p.x, p.y, p.z] for p in landmarks], dtype=np.float32)
    pts -= pts[0]
    scale = np.max(np.linalg.norm(pts[:, :2], axis=1))
    if scale < 1e-6:
        return None
    pts /= scale
    return pts.flatten()

1. Coordinate Frames and Initial Geometry ($t = 0$)
Let $\{\hat{E}_x, \hat{E}_y, \hat{E}_z\}$ be the fixed inertial (lab) basis, $\{\hat{x}(t), \hat{y}(t), \hat{z}(t)\}$ be the rotating unprimed orthonormal basis, and $\{\hat{x}'(t), \hat{y}'(t), \hat{z}'(t)\}$ be the rotating primed orthonormal basis, all sharing the origin $O$.
1. Unprimed circle (lies in the unprimed $yz$-plane, normal $\hat{x}(t)$):
$$\mathbf{r}(\phi, t) = R\cos\phi\,\hat{y}(t) + R\sin\phi\,\hat{z}(t)$$
The point to be traced on the sphere of radius $R$ is the $+z$ pole ($\phi = \frac{\pi}{2}$):
$$\mathbf{P}(t) = R\,\hat{z}(t)$$
2. Primed circle (lies in the primed $y'z'$-plane, normal $\hat{x}'(t)$):
$$\mathbf{r}'(\phi', t) = R\cos\phi'\,\hat{y}'(t) + R\sin\phi'\,\hat{z}'(t)$$
3. The $z = 0$ Dynamic Plane and Line of Intersection:
- In the unprimed frame, a plane perpendicular to the unprimed circle's plane ($x=0$) at height $z \in [-R, R]$ is given by $\mathbf{r} \cdot \hat{z}(t) = z$.
- At $z = \pm R$, it is tangent to the unprimed circle at a single point $\pm R\hat{z}(t)$.
- At $z = 0$, it is the unprimed $xy$-plane ($\mathbf{r} \cdot \hat{z}(t) = 0$), which intersects the unprimed circle at the two antipodal points $\pm R\hat{y}(t)$ ($\phi = 0, \pi$).
- Since the two circles intersect in this $z = 0$ plane, the unit vector across the two intersecting points (the line of nodes) is $\hat{y}(t)$.
4. Inter-plane Angle ($\alpha = 45^\circ = \frac{\pi}{4}$):
Since both normals $\hat{x}(t)$ and $\hat{x}'(t)$ are perpendicular to the intersection line $\hat{y}(t)$, the $45^\circ$ angle between the two circle planes means:
$$\hat{x}(t) \cdot \hat{x}'(t) = \cos\alpha = \frac{\sqrt{2}}{2}$$
Taking the unprimed frame aligned with the inertial frame at $t = 0$, i.e., $\hat{x}(0)=\hat{E}_x,\ \hat{y}(0)=\hat{E}_y,\ \hat{z}(0)=\hat{E}_z$, the initial primed normal is tilted by $\alpha = \frac{\pi}{4}$ about $\hat{E}_y$:
$$\hat{x}'(0) = R_y(-\alpha)\hat{E}_x = \cos\alpha\,\hat{E}_x + \sin\alpha\,\hat{E}_z = \frac{\sqrt{2}}{2}\begin{bmatrix} 1 \\ 0 \\ 1 \end{bmatrix}$$
2. Coupling the Two Rotations ($\omega_1 = \omega$ and $\omega_2 = \frac{\omega}{4}$)
There is a key kinematic distinction in how the two rotations combine in 3D:
Case A: Hierarchical / Precessing Coupling (Dynamic $\hat{x}'(t)$ — Non-trivial Gyroscopic Trace)
Here, the primed circle rotates at rate $\omega_2 = \frac{\omega}{4}$ about the intersection axis $\hat{E}_y$ in the $z=0$ plane, making the primed normal a dynamic vector:
$$\hat{x}'(t) = R_y\!\left(\frac{\omega}{4}t - \alpha\right)\hat{E}_x = \begin{bmatrix} \cos\!\left(\frac{\omega}{4}t - \frac{\pi}{4}\right) \\[4pt] 0 \\[4pt] -\sin\!\left(\frac{\omega}{4}t - \frac{\pi}{4}\right) \end{bmatrix}$$
Simultaneously, the unprimed circle (maintaining a constant $\alpha = 45^\circ$ angle to the primed plane) rotates at rate $\omega_1 = \omega$ about this dynamic normal $\hat{x}'(t)$.
The total rotation matrix of the unprimed frame is:
$$R(t) = R_y\!\left(\frac{\omega}{4}t - \alpha\right) R_x(\omega t)\, R_y(\alpha)$$
where:
- $R(0) = I_3$, so $\mathbf{P}(0) = (0, 0, R)^T$.
- $\hat{x}(t) \cdot \hat{x}'(t) = \cos\alpha = \frac{\sqrt{2}}{2}$ is strictly constant ($45^\circ$) for all $t$.
- The intersection line of the two circles is always $\pm R\hat{y}(t)$ (in the $z=0$ unprimed plane) since $\hat{y}(t) \perp \hat{x}(t)$ and $\hat{y}(t) \perp \hat{x}'(t)$ for all $t$.
- The angular velocity vector is:
$$\boldsymbol{\Omega}(t) = \frac{\omega}{4}\hat{E}_y + \omega\,\hat{x}'(t)$$
Explicit Trajectory of $\mathbf{P}(t) = R\,\hat{z}(t) = R\,R(t)\hat{E}_z$:
$$\mathbf{P}(t) = R\begin{bmatrix}
\sin\alpha\cos\!\left(\frac{\omega}{4}t - \alpha\right) + \cos\alpha\sin\!\left(\frac{\omega}{4}t - \alpha\right)\cos(\omega t) \\[6pt]
-\cos\alpha\sin(\omega t) \\[6pt]
-\sin\alpha\sin\!\left(\frac{\omega}{4}t - \alpha\right) + \cos\alpha\cos\!\left(\frac{\omega}{4}t - \alpha\right)\cos(\omega t)
\end{bmatrix}$$
Substituting $\alpha = \frac{\pi}{4}$ ($\sin\alpha = \cos\alpha = \frac{\sqrt{2}}{2}$):
$$\boxed{
\begin{aligned}
X(t) &= \frac{\sqrt{2}}{2}R\left[\cos\!\left(\frac{\omega}{4}t - \frac{\pi}{4}\right) + \sin\!\left(\frac{\omega}{4}t - \frac{\pi}{4}\right)\cos(\omega t)\right] \\
Y(t) &= -\frac{\sqrt{2}}{2}R\sin(\omega t) \\
Z(t) &= \frac{\sqrt{2}}{2}R\left[-\sin\!\left(\frac{\omega}{4}t - \frac{\pi}{4}\right) + \cos\!\left(\frac{\omega}{4}t - \frac{\pi}{4}\right)\cos(\omega t)\right]
\end{aligned}
}$$
This traces a closed, 4-lobed spherical curve (periodic with period $T = \frac{8\pi}{\omega}$) on the sphere $X^2 + Y^2 + Z^2 = R^2$.
Case B: Reversed Hierarchy (Unprimed rotation carries the $z=0$ intersection axis $\hat{y}(t)$)
If instead the unprimed rotation at rate $\omega$ about $\hat{x}'$ carries the intersection vector $\hat{y}(t)$ around $\hat{x}'$, and the $\frac{\omega}{4}$ rotation acts about that moving intersection vector $\hat{y}(t)$:
$$R(t) = R_y(-\alpha)\, R_x(\omega t)\, R_y\!\left(\frac{\omega}{4}t + \alpha\right)$$
Applying this to $\mathbf{P}(t) = R\,R(t)\hat{E}_z$ with $\alpha = \frac{\pi}{4}$ gives:
$$\boxed{
\begin{aligned}
X(t) &= \frac{\sqrt{2}}{2}R\left[\sin\!\left(\frac{\omega}{4}t + \frac{\pi}{4}\right) - \cos\!\left(\frac{\omega}{4}t + \frac{\pi}{4}\right)\cos(\omega t)\right] \\
Y(t) &= -\sin(\omega t)\cos\!\left(\frac{\omega}{4}t + \frac{\pi}{4}\right) R \\
Z(t) &= \frac{\sqrt{2}}{2}R\left[\sin\!\left(\frac{\omega}{4}t + \frac{\pi}{4}\right) + \cos\!\left(\frac{\omega}{4}t + \frac{\pi}{4}\right)\cos(\omega t)\right]
\end{aligned}
}$$
Note on Mutual Body-Locked Instantaneous Addition ($\boldsymbol{\Omega} = \omega\hat{x}'(t) + \frac{\omega}{4}\hat{y}(t)$)
If $\hat{x}'(t)$ only rotates about $\hat{y}(t)$ at $\frac{\omega}{4}$ ($\dot{\hat{x}}' = \frac{\omega}{4}\hat{y} \times \hat{x}'$) and $\hat{y}(t)$ only rotates about $\hat{x}'(t)$ at $\omega$ ($\dot{\hat{y}} = \omega\hat{x}' \times \hat{y}$) simultaneously with both axes locked in the unprimed frame, then:
$$\frac{d\boldsymbol{\Omega}}{dt} = \omega\dot{\hat{x}}' + \frac{\omega}{4}\dot{\hat{y}} = \frac{\omega^2}{4}(\hat{y} \times \hat{x}' + \hat{x}' \times \hat{y}) = \mathbf{0}$$
In that degenerate case, the two cross-precessions cancel identically and $\boldsymbol{\Omega}$ stays fixed in space (tracing only a flat circle). Thus Case A (or Case B) is required for a true dynamic two-axis precession trace.
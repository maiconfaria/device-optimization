# Coupler desing

# Remeber that:
    Courant [number]
    Specify the Courant factor S which relates the time step size to the spatial discretization: cΔt = SΔx. Default is 0.5. For numerical stability, the Courant factor must be at most n_\textrm{min}/\sqrt{\textrm{\# dimensions}}, where nmin is the minimum refractive index (usually 1), and in practice S should be slightly smaller.

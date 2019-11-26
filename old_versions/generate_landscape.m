[X1,X2] = ndgrid((0:20:100));
[Xq1, Xq2] = ndgrid((0:1:100));

V = rand(6,6);

Vq = interpn(X1, X2, V, Xq1, Xq2, 'cubic');

mesh(Vq);
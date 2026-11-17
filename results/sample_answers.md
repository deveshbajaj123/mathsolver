# Rendered sample answers

These are machine generated and still require presentation review.

## PD-MATH-VII-002

20.

In the given diagram, $\triangle PQR$ is an isosceles triangle. S and T are the midpoints of PQ and PR respectively. Prove that $RS = QT$.

**Solution**

Since $S$ and $T$ are midpoints, $PS=\tfrac12 PQ$ and $PT=\tfrac12 PR$. The isosceles condition $PQ=PR$ therefore gives $PS=PT$.

Also, $\angle RPS=\angle QPT$: both are the angle at $P$ between $PQ$ and $PR$.

Thus $\triangle PRS\cong\triangle PQT$ by SAS, with $PR=PQ$, $PS=PT$, and equal included angles. Corresponding sides give $RS=QT$.

## PD-MATH-VIII-001

10. If a + b + c = 5 and ab + bc + ca = 10 then prove that a³ + b³ + c³ - 3abc = -25

**Solution**

Given: $a + b + c = 5$ and $a b + b c + c a = 10$.

**LHS:**

$$a^{3} + b^{3} + c^{3} - 3 a b c$$

$$= \left(a + b + c\right)^{3} - 3 \left(a + b + c\right) \left(a b + a c + b c\right)$$

*Write the expression in terms of the sum, the sum of products and the product of the variables.*

$$= -25$$

*Use the givens $a + b + c = 5$, $a b + a c + b c = 10$.*

This is the RHS, so LHS = RHS. Hence proved.

## PD-MATH-VIII-002

If x + 1/x = 2, Prove that x² + 1/x² = x³ + 1/x³ = x⁴ + 1/x⁴

**Solution**

**Part 1: $x^{2} + \frac{1}{x^{2}} = x^{3} + \frac{1}{x^{3}}$**

Given: $x + \frac{1}{x} = 2$.

From the given condition:

$$x + \frac{1}{x} = 2 \implies x^{2} + 1 = 2 x$$

*Cross-multiply to clear the denominators.*

$$x^{2} + 1 = 2 x \implies x^{2} - 2 x + 1 = 0$$

*Bring every term to one side and expand.*

$$x^{2} - 2 x + 1 = 0 \implies \left(x - 1\right)^{2} = 0$$

*Factorise.*

$$\left(x - 1\right)^{2} = 0 \implies x - 1 = 0$$

*A product is zero only if a factor is zero, and the other factors are nonzero, so $x - 1 = 0$.*

$$x - 1 = 0 \implies x = 1$$

*Make $x$ the subject.*

**LHS:**

$$x^{2} + \frac{1}{x^{2}}$$

$$= 2$$

*Substitute $x = 1$.*

**RHS:**

$$x^{3} + \frac{1}{x^{3}}$$

$$= 2$$

*Substitute $x = 1$.*

Both sides reduce to the same expression, so LHS = RHS. Hence proved.

Valid where $x \neq 0$.

**Part 2: $x^{3} + \frac{1}{x^{3}} = x^{4} + \frac{1}{x^{4}}$**

Given: $x + \frac{1}{x} = 2$.

From the earlier part: $x^{2} + \frac{1}{x^{2}} = x^{3} + \frac{1}{x^{3}}$.

From the given condition:

$$x^{2} + \frac{1}{x^{2}} = x^{3} + \frac{1}{x^{3}} \implies x^{3} \left(x^{4} + 1\right) = x^{2} \left(x^{6} + 1\right)$$

*Cross-multiply to clear the denominators.*

$$x^{3} \left(x^{4} + 1\right) = x^{2} \left(x^{6} + 1\right) \implies - x^{8} + x^{7} + x^{3} - x^{2} = 0$$

*Bring every term to one side and expand.*

$$- x^{8} + x^{7} + x^{3} - x^{2} = 0 \implies - x^{2} \left(x - 1\right)^{2} \left(x^{4} + x^{3} + x^{2} + x + 1\right) = 0$$

*Factorise.*

$$- x^{2} \left(x - 1\right)^{2} \left(x^{4} + x^{3} + x^{2} + x + 1\right) = 0 \implies x - 1 = 0$$

*A product is zero only if a factor is zero, and the other factors are nonzero, so $x - 1 = 0$.*

$$x - 1 = 0 \implies x = 1$$

*Make $x$ the subject.*

**LHS:**

$$x^{3} + \frac{1}{x^{3}}$$

$$= 2$$

*Substitute $x = 1$.*

**RHS:**

$$x^{4} + \frac{1}{x^{4}}$$

$$= 2$$

*Substitute $x = 1$.*

Both sides reduce to the same expression, so LHS = RHS. Hence proved.

Valid where $x \neq 0$.

## PD-MATH-VIII-005

Q.8(a) Show that : $(x^{a+b})^{a-b} \times (x^{b+c})^{b-c} \times (x^{c+a})^{c-a} = 1$ [4]

**Solution**

**LHS:**

$$\left(x^{a + b}\right)^{a - b} \left(x^{b + c}\right)^{b - c} \left(x^{c + a}\right)^{c - a}$$

$$= x^{\left(- a + c\right) \left(a + c\right)} x^{\left(a - b\right) \left(a + b\right)} x^{\left(b - c\right) \left(b + c\right)}$$

*Use $(x^m)^n = x^{mn}$.*

$$= x^{\left(- a + c\right) \left(a + c\right) + \left(a - b\right) \left(a + b\right) + \left(b - c\right) \left(b + c\right)}$$

*Use $x^m \cdot x^n = x^{m+n}$.*

$$= 1$$

*Simplify the index.*

This is the RHS, so LHS = RHS. Hence proved.

## PD-MATH-IX-001

28. Show that if the diagonals of a quadrilateral bisect each other at right angles, then it is a rhombus.

**Solution**

**Part 1: $AB^{2} = BC^{2}$**

Take coordinates: $O = \left(0, 0\right)$, $A = \left(p, 0\right)$, $C = \left(- p, 0\right)$, $B = \left(0, q\right)$, $D = \left(0, - q\right)$.

*The diagonals meet at O, taken as the origin, along the axes. Equal squared lengths give equal sides, so ABCD is a rhombus.*

These coordinates give: O is the midpoint of AC; O is the midpoint of BD; AC ⊥ BD.

Then:

$$AB^{2} = \left(0 - p\right)^{2} + \left(q\right)^{2} = p^{2} + q^{2}$$

$$BC^{2} = \left(- p\right)^{2} + \left(0 - q\right)^{2} = p^{2} + q^{2}$$

**LHS:**

$$AB^{2}$$

$$= p^{2} + q^{2}$$

*Write each length, area or product in coordinates (see above).*

**RHS:**

$$BC^{2}$$

$$= p^{2} + q^{2}$$

*Write each length, area or product in coordinates (see above).*

Both sides reduce to the same expression, so LHS = RHS. Hence proved.

**Part 2: $BC^{2} = CD^{2}$**

Take coordinates: $O = \left(0, 0\right)$, $A = \left(p, 0\right)$, $C = \left(- p, 0\right)$, $B = \left(0, q\right)$, $D = \left(0, - q\right)$.

*The diagonals meet at O, taken as the origin, along the axes. Equal squared lengths give equal sides, so ABCD is a rhombus.*

These coordinates give: O is the midpoint of AC; O is the midpoint of BD; AC ⊥ BD.

Then:

$$BC^{2} = \left(- p\right)^{2} + \left(0 - q\right)^{2} = p^{2} + q^{2}$$

$$CD^{2} = \left(0 - \left(- p\right)\right)^{2} + \left(- q\right)^{2} = p^{2} + q^{2}$$

From the earlier part: $AB^{2} = BC^{2}$.

**LHS:**

$$BC^{2}$$

$$= p^{2} + q^{2}$$

*Write each length, area or product in coordinates (see above).*

**RHS:**

$$CD^{2}$$

$$= p^{2} + q^{2}$$

*Write each length, area or product in coordinates (see above).*

Both sides reduce to the same expression, so LHS = RHS. Hence proved.

**Part 3: $CD^{2} = DA^{2}$**

Take coordinates: $O = \left(0, 0\right)$, $A = \left(p, 0\right)$, $C = \left(- p, 0\right)$, $B = \left(0, q\right)$, $D = \left(0, - q\right)$.

*The diagonals meet at O, taken as the origin, along the axes. Equal squared lengths give equal sides, so ABCD is a rhombus.*

These coordinates give: O is the midpoint of AC; O is the midpoint of BD; AC ⊥ BD.

Then:

$$CD^{2} = \left(0 - \left(- p\right)\right)^{2} + \left(- q\right)^{2} = p^{2} + q^{2}$$

$$DA^{2} = \left(p\right)^{2} + \left(0 - \left(- q\right)\right)^{2} = p^{2} + q^{2}$$

From the earlier part: $AB^{2} = BC^{2}$.

From the earlier part: $BC^{2} = CD^{2}$.

**LHS:**

$$CD^{2}$$

$$= p^{2} + q^{2}$$

*Write each length, area or product in coordinates (see above).*

**RHS:**

$$DA^{2}$$

$$= p^{2} + q^{2}$$

*Write each length, area or product in coordinates (see above).*

Both sides reduce to the same expression, so LHS = RHS. Hence proved.

## PD-MATH-IX-004

35. Show that quadrilateral formed by joining the mid points of the pairs of adjacent sides of a square is also a square.

**Solution**

**Part 1: $PQ^{2} = QR^{2}$**

Take coordinates: $A = \left(0, 0\right)$, $B = \left(2 a, 0\right)$, $C = \left(2 a, 2 a\right)$, $D = \left(0, 2 a\right)$, $P = \left(a, 0\right)$, $Q = \left(2 a, a\right)$, $R = \left(a, 2 a\right)$, $S = \left(0, a\right)$.

*Square of side 2a. Four equal sides and a right angle at Q (the dot product of QP and QR is 0) make PQRS a square.*

These coordinates give: ∠DAB = 90°; ∠ABC = 90°; AB = BC; BC = CD; P is the midpoint of AB; Q is the midpoint of BC; R is the midpoint of CD; S is the midpoint of DA.

Then:

$$PQ^{2} = \left(2 a - a\right)^{2} + \left(a\right)^{2} = 2 a^{2}$$

$$QR^{2} = \left(a - 2 a\right)^{2} + \left(2 a - a\right)^{2} = 2 a^{2}$$

**LHS:**

$$PQ^{2}$$

$$= 2 a^{2}$$

*Write each length, area or product in coordinates (see above).*

**RHS:**

$$QR^{2}$$

$$= 2 a^{2}$$

*Write each length, area or product in coordinates (see above).*

Both sides reduce to the same expression, so LHS = RHS. Hence proved.

**Part 2: $QR^{2} = RS^{2}$**

Take coordinates: $A = \left(0, 0\right)$, $B = \left(2 a, 0\right)$, $C = \left(2 a, 2 a\right)$, $D = \left(0, 2 a\right)$, $P = \left(a, 0\right)$, $Q = \left(2 a, a\right)$, $R = \left(a, 2 a\right)$, $S = \left(0, a\right)$.

*Square of side 2a. Four equal sides and a right angle at Q (the dot product of QP and QR is 0) make PQRS a square.*

These coordinates give: ∠DAB = 90°; ∠ABC = 90°; AB = BC; BC = CD; P is the midpoint of AB; Q is the midpoint of BC; R is the midpoint of CD; S is the midpoint of DA.

Then:

$$QR^{2} = \left(a - 2 a\right)^{2} + \left(2 a - a\right)^{2} = 2 a^{2}$$

$$RS^{2} = \left(0 - a\right)^{2} + \left(a - 2 a\right)^{2} = 2 a^{2}$$

From the earlier part: $PQ^{2} = QR^{2}$.

**LHS:**

$$QR^{2}$$

$$= 2 a^{2}$$

*Write each length, area or product in coordinates (see above).*

**RHS:**

$$RS^{2}$$

$$= 2 a^{2}$$

*Write each length, area or product in coordinates (see above).*

Both sides reduce to the same expression, so LHS = RHS. Hence proved.

**Part 3: $RS^{2} = SP^{2}$**

Take coordinates: $A = \left(0, 0\right)$, $B = \left(2 a, 0\right)$, $C = \left(2 a, 2 a\right)$, $D = \left(0, 2 a\right)$, $P = \left(a, 0\right)$, $Q = \left(2 a, a\right)$, $R = \left(a, 2 a\right)$, $S = \left(0, a\right)$.

*Square of side 2a. Four equal sides and a right angle at Q (the dot product of QP and QR is 0) make PQRS a square.*

These coordinates give: ∠DAB = 90°; ∠ABC = 90°; AB = BC; BC = CD; P is the midpoint of AB; Q is the midpoint of BC; R is the midpoint of CD; S is the midpoint of DA.

Then:

$$RS^{2} = \left(0 - a\right)^{2} + \left(a - 2 a\right)^{2} = 2 a^{2}$$

$$SP^{2} = \left(a\right)^{2} + \left(0 - a\right)^{2} = 2 a^{2}$$

From the earlier part: $PQ^{2} = QR^{2}$.

From the earlier part: $QR^{2} = RS^{2}$.

**LHS:**

$$RS^{2}$$

$$= 2 a^{2}$$

*Write each length, area or product in coordinates (see above).*

**RHS:**

$$SP^{2}$$

$$= 2 a^{2}$$

*Write each length, area or product in coordinates (see above).*

Both sides reduce to the same expression, so LHS = RHS. Hence proved.

**Part 4: $\overrightarrow{QP} \cdot \overrightarrow{QR} = 0$**

Take coordinates: $A = \left(0, 0\right)$, $B = \left(2 a, 0\right)$, $C = \left(2 a, 2 a\right)$, $D = \left(0, 2 a\right)$, $P = \left(a, 0\right)$, $Q = \left(2 a, a\right)$, $R = \left(a, 2 a\right)$, $S = \left(0, a\right)$.

*Square of side 2a. Four equal sides and a right angle at Q (the dot product of QP and QR is 0) make PQRS a square.*

These coordinates give: ∠DAB = 90°; ∠ABC = 90°; AB = BC; BC = CD; P is the midpoint of AB; Q is the midpoint of BC; R is the midpoint of CD; S is the midpoint of DA.

Then:

$$\overrightarrow{QP} \cdot \overrightarrow{QR} = \left(a - 2 a\right)\left(a - 2 a\right) + \left(0 - a\right)\left(2 a - a\right) = 0$$

From the earlier part: $PQ^{2} = QR^{2}$.

From the earlier part: $QR^{2} = RS^{2}$.

From the earlier part: $RS^{2} = SP^{2}$.

**LHS:**

$$\overrightarrow{QP} \cdot \overrightarrow{QR}$$

$$= 0$$

*Write each length, area or product in coordinates (see above).*

This is the RHS, so LHS = RHS. Hence proved.

## PD-MATH-IX-005

(c) Prove that: $$7 \log \frac{16}{15} + 5 \log \frac{25}{24} + 3 \log \frac{81}{80} = \log 2.$$ [4]

**Solution**

**LHS:**

$$7 log\left(\frac{16}{15}\right) + 5 log\left(\frac{25}{24}\right) + 3 log\left(\frac{81}{80}\right)$$

$$= 3 \left(- 4 \log{\left(2 \right)} - \log{\left(5 \right)} + 4 \log{\left(3 \right)}\right) + 5 \left(- 3 \log{\left(2 \right)} - \log{\left(3 \right)} + 2 \log{\left(5 \right)}\right) + 7 \left(- \log{\left(5 \right)} - \log{\left(3 \right)} + 4 \log{\left(2 \right)}\right)$$

*Write each logarithm in terms of the logs of primes.*

$$= \left(- 12 \log{\left(2 \right)} - 3 \log{\left(5 \right)} + 12 \log{\left(3 \right)}\right) - \left(- 10 \log{\left(5 \right)} + 5 \log{\left(3 \right)} + 15 \log{\left(2 \right)}\right) - \left(- 28 \log{\left(2 \right)} + 7 \log{\left(3 \right)} + 7 \log{\left(5 \right)}\right)$$

*Cancel.*

$$= \log{\left(2 \right)}$$

*Cancel.*

This is the RHS, so LHS = RHS. Hence proved.

## PD-MATH-IX-006

(b). In a parallelogram ABCD, points \( M \) and \( N \) have been taken on opposite sides AB and CD respectively such that \( AM = CN \). Show that \( AC \) and \( MN \) bisect each other. [3]

**Solution**

**Part 1: $\frac{x_{A} + x_{C}}{2} = \frac{x_{M} + x_{N}}{2}$**

Take coordinates: $A = \left(0, 0\right)$, $B = \left(b, 0\right)$, $D = \left(p, q\right)$, $C = \left(b + p, q\right)$, $M = \left(m, 0\right)$, $N = \left(b - m + p, q\right)$.

*A at the origin, AB along the x-axis. The midpoints of AC and MN have the same coordinates, so the diagonals bisect each other.*

These coordinates give: AB ∥ DC; AD ∥ BC; M lies on line AB; N lies on line CD; AM = CN.

Then:

**LHS:**

$$\frac{x_{A} + x_{C}}{2}$$

$$= \frac{b}{2} + \frac{p}{2}$$

*Write each length, area or product in coordinates (see above).*

**RHS:**

$$\frac{x_{M} + x_{N}}{2}$$

$$= \frac{b}{2} + \frac{p}{2}$$

*Write each length, area or product in coordinates (see above).*

Both sides reduce to the same expression, so LHS = RHS. Hence proved.

**Part 2: $\frac{y_{A} + y_{C}}{2} = \frac{y_{M} + y_{N}}{2}$**

Take coordinates: $A = \left(0, 0\right)$, $B = \left(b, 0\right)$, $D = \left(p, q\right)$, $C = \left(b + p, q\right)$, $M = \left(m, 0\right)$, $N = \left(b - m + p, q\right)$.

*A at the origin, AB along the x-axis. The midpoints of AC and MN have the same coordinates, so the diagonals bisect each other.*

These coordinates give: AB ∥ DC; AD ∥ BC; M lies on line AB; N lies on line CD; AM = CN.

Then:

From the earlier part: $\frac{x_{A}}{2} + \frac{x_{C}}{2} = \frac{x_{M}}{2} + \frac{x_{N}}{2}$.

**LHS:**

$$\frac{y_{A} + y_{C}}{2}$$

$$= \frac{q}{2}$$

*Write each length, area or product in coordinates (see above).*

**RHS:**

$$\frac{y_{M} + y_{N}}{2}$$

$$= \frac{q}{2}$$

*Write each length, area or product in coordinates (see above).*

Both sides reduce to the same expression, so LHS = RHS. Hence proved.

## PD-MATH-IX-007

(c). In ΔABC, ∠ABC = 90°. If D and E are the mid-points of the sides BC and AB respectively, prove that AD² + CE² = 5 DE². [4]

**Solution**

Take coordinates: $B = \left(0, 0\right)$, $A = \left(0, 2 a\right)$, $C = \left(2 c, 0\right)$, $D = \left(c, 0\right)$, $E = \left(0, a\right)$.

*B at the origin, BC along the x-axis and BA along the y-axis.*

These coordinates give: ∠ABC = 90°; D is the midpoint of BC; E is the midpoint of AB.

Then:

$$AD^{2} = \left(c\right)^{2} + \left(0 - 2 a\right)^{2} = 4 a^{2} + c^{2}$$

$$CE^{2} = \left(0 - 2 c\right)^{2} + \left(a\right)^{2} = a^{2} + 4 c^{2}$$

$$DE^{2} = \left(0 - c\right)^{2} + \left(a\right)^{2} = a^{2} + c^{2}$$

**LHS:**

$$AD^{2} + CE^{2}$$

$$= 5 a^{2} + 5 c^{2}$$

*Write each length, area or product in coordinates (see above).*

**RHS:**

$$5 DE^{2}$$

$$= 5 a^{2} + 5 c^{2}$$

*Write each length, area or product in coordinates (see above).*

Both sides reduce to the same expression, so LHS = RHS. Hence proved.

## PD-MATH-IX-009

(iii) In the given figure, ABCD is a quadrilateral in which P,Q,R and S are mid-points of AB, BC, CD and DA respectively. AC is its diagonal. Show that

(a) \(\mathrm{SR} \parallel \mathrm{AC}, \mathrm{SR} = \frac{1}{2} \mathrm{AC}\)
(b) \(\mathrm{PQ} = \mathrm{SR}\)
(c) PQRS is a parallelogram

[4]

**Solution**

**Part 1: $\overrightarrow{SR} \times \overrightarrow{AC} = 0$**

Take coordinates: $A = \left(0, 0\right)$, $B = \left(2 b_{1}, 2 b_{2}\right)$, $C = \left(2 c_{1}, 2 c_{2}\right)$, $D = \left(2 d_{1}, 2 d_{2}\right)$, $P = \left(b_{1}, b_{2}\right)$, $Q = \left(b_{1} + c_{1}, b_{2} + c_{2}\right)$, $R = \left(c_{1} + d_{1}, c_{2} + d_{2}\right)$, $S = \left(d_{1}, d_{2}\right)$.

*Any quadrilateral, A at the origin. A zero cross product means parallel. (c) follows from PQ ∥ SR and PQ = SR.*

These coordinates give: P is the midpoint of AB; Q is the midpoint of BC; R is the midpoint of CD; S is the midpoint of DA.

Then:

$$\overrightarrow{SR} \times \overrightarrow{AC} = \left(c_{1} + d_{1} - d_{1}\right)\left(2 c_{2}\right) - \left(c_{2} + d_{2} - d_{2}\right)\left(2 c_{1}\right) = 0$$

**LHS:**

$$\overrightarrow{SR} \times \overrightarrow{AC}$$

$$= 0$$

*Write each length, area or product in coordinates (see above).*

This is the RHS, so LHS = RHS. Hence proved.

**Part 2: $SR^{2} = \frac{AC^{2}}{4}$**

Take coordinates: $A = \left(0, 0\right)$, $B = \left(2 b_{1}, 2 b_{2}\right)$, $C = \left(2 c_{1}, 2 c_{2}\right)$, $D = \left(2 d_{1}, 2 d_{2}\right)$, $P = \left(b_{1}, b_{2}\right)$, $Q = \left(b_{1} + c_{1}, b_{2} + c_{2}\right)$, $R = \left(c_{1} + d_{1}, c_{2} + d_{2}\right)$, $S = \left(d_{1}, d_{2}\right)$.

*Any quadrilateral, A at the origin. A zero cross product means parallel. (c) follows from PQ ∥ SR and PQ = SR.*

These coordinates give: P is the midpoint of AB; Q is the midpoint of BC; R is the midpoint of CD; S is the midpoint of DA.

Then:

$$AC^{2} = \left(2 c_{1}\right)^{2} + \left(2 c_{2}\right)^{2} = 4 \left(c_{1}^{2} + c_{2}^{2}\right)$$

$$SR^{2} = \left(c_{1} + d_{1} - d_{1}\right)^{2} + \left(c_{2} + d_{2} - d_{2}\right)^{2} = c_{1}^{2} + c_{2}^{2}$$

From the earlier part: $\overrightarrow{SR} \times \overrightarrow{AC} = 0$.

**LHS:**

$$SR^{2}$$

$$= c_{1}^{2} + c_{2}^{2}$$

*Write each length, area or product in coordinates (see above).*

**RHS:**

$$\frac{AC^{2}}{4}$$

$$= c_{1}^{2} + c_{2}^{2}$$

*Write each length, area or product in coordinates (see above).*

Both sides reduce to the same expression, so LHS = RHS. Hence proved.

**Part 3: $PQ^{2} = SR^{2}$**

Take coordinates: $A = \left(0, 0\right)$, $B = \left(2 b_{1}, 2 b_{2}\right)$, $C = \left(2 c_{1}, 2 c_{2}\right)$, $D = \left(2 d_{1}, 2 d_{2}\right)$, $P = \left(b_{1}, b_{2}\right)$, $Q = \left(b_{1} + c_{1}, b_{2} + c_{2}\right)$, $R = \left(c_{1} + d_{1}, c_{2} + d_{2}\right)$, $S = \left(d_{1}, d_{2}\right)$.

*Any quadrilateral, A at the origin. A zero cross product means parallel. (c) follows from PQ ∥ SR and PQ = SR.*

These coordinates give: P is the midpoint of AB; Q is the midpoint of BC; R is the midpoint of CD; S is the midpoint of DA.

Then:

$$PQ^{2} = \left(b_{1} + c_{1} - b_{1}\right)^{2} + \left(b_{2} + c_{2} - b_{2}\right)^{2} = c_{1}^{2} + c_{2}^{2}$$

$$SR^{2} = \left(c_{1} + d_{1} - d_{1}\right)^{2} + \left(c_{2} + d_{2} - d_{2}\right)^{2} = c_{1}^{2} + c_{2}^{2}$$

From the earlier part: $\overrightarrow{SR} \times \overrightarrow{AC} = 0$.

From the earlier part: $SR^{2} = \frac{AC^{2}}{4}$.

**LHS:**

$$PQ^{2}$$

$$= c_{1}^{2} + c_{2}^{2}$$

*Write each length, area or product in coordinates (see above).*

**RHS:**

$$SR^{2}$$

$$= c_{1}^{2} + c_{2}^{2}$$

*Write each length, area or product in coordinates (see above).*

Both sides reduce to the same expression, so LHS = RHS. Hence proved.

**Part 4: $\overrightarrow{PQ} \times \overrightarrow{SR} = 0$**

Take coordinates: $A = \left(0, 0\right)$, $B = \left(2 b_{1}, 2 b_{2}\right)$, $C = \left(2 c_{1}, 2 c_{2}\right)$, $D = \left(2 d_{1}, 2 d_{2}\right)$, $P = \left(b_{1}, b_{2}\right)$, $Q = \left(b_{1} + c_{1}, b_{2} + c_{2}\right)$, $R = \left(c_{1} + d_{1}, c_{2} + d_{2}\right)$, $S = \left(d_{1}, d_{2}\right)$.

*Any quadrilateral, A at the origin. A zero cross product means parallel. (c) follows from PQ ∥ SR and PQ = SR.*

These coordinates give: P is the midpoint of AB; Q is the midpoint of BC; R is the midpoint of CD; S is the midpoint of DA.

Then:

$$\overrightarrow{PQ} \times \overrightarrow{SR} = \left(b_{1} + c_{1} - b_{1}\right)\left(c_{2} + d_{2} - d_{2}\right) - \left(b_{2} + c_{2} - b_{2}\right)\left(c_{1} + d_{1} - d_{1}\right) = 0$$

From the earlier part: $\overrightarrow{SR} \times \overrightarrow{AC} = 0$.

From the earlier part: $SR^{2} = \frac{AC^{2}}{4}$.

From the earlier part: $PQ^{2} = SR^{2}$.

**LHS:**

$$\overrightarrow{PQ} \times \overrightarrow{SR}$$

$$= 0$$

*Write each length, area or product in coordinates (see above).*

This is the RHS, so LHS = RHS. Hence proved.

## PD-MATH-IX-013

b) The area of three adjacent faces of a cuboid are x, y and z. if the volume is V, prove that V² = XYZ. [3]

**Solution**

Given: $x = l b$ and $y = b h$ and $z = h l$ and $V = l b h$.

From the givens:

$$V = b h l \implies V = b h l$$

*Make $V$ the subject.*

$$z = h l \implies h = \frac{z}{l}$$

*Make $h$ the subject.*

$$y = b h \implies y = b h$$

*Make $y$ the subject.*

$$x = b l \implies x = b l$$

*Make $x$ the subject.*

**LHS:**

$$V^{2}$$

$$= b^{2} z^{2}$$

*Substitute $V = b h l$ and $h = \frac{z}{l}$.*

**RHS:**

$$x y z$$

$$= b^{2} z^{2}$$

*Substitute $x = b l$ and $y = b h$ and $h = \frac{z}{l}$.*

Both sides reduce to the same expression, so LHS = RHS. Hence proved.

## PD-MATH-IX-014

b) M and N are points on sides QR and PQ respectively of $$\Delta PQR$$, right angled at Q. prove that:

$$PM^2 + RN^2 = PR^2 + MN^2$$ [3]

**Solution**

Take coordinates: $Q = \left(0, 0\right)$, $P = \left(0, p\right)$, $R = \left(r, 0\right)$, $M = \left(m, 0\right)$, $N = \left(0, n\right)$.

*Q at the origin, QR along the x-axis and QP along the y-axis.*

These coordinates give: ∠PQR = 90°; M lies on line QR; N lies on line PQ.

Then:

$$MN^{2} = \left(0 - m\right)^{2} + \left(n\right)^{2} = m^{2} + n^{2}$$

$$PM^{2} = \left(m\right)^{2} + \left(0 - p\right)^{2} = m^{2} + p^{2}$$

$$PR^{2} = \left(r\right)^{2} + \left(0 - p\right)^{2} = p^{2} + r^{2}$$

$$RN^{2} = \left(0 - r\right)^{2} + \left(n\right)^{2} = n^{2} + r^{2}$$

**LHS:**

$$PM^{2} + RN^{2}$$

$$= m^{2} + n^{2} + p^{2} + r^{2}$$

*Write each length, area or product in coordinates (see above).*

**RHS:**

$$PR^{2} + MN^{2}$$

$$= m^{2} + n^{2} + p^{2} + r^{2}$$

*Write each length, area or product in coordinates (see above).*

Both sides reduce to the same expression, so LHS = RHS. Hence proved.

## PD-MATH-IX-015

c) If $$abc = 1$$ , show that $$\frac{1}{1+a+b^{-1}} + \frac{1}{1+b+c^{-1}} + \frac{1}{1+c+a^{-1}} = 1$$ . [4]

**Solution**

Given: $a b c = 1$.

From the given condition:

$$a b c = 1 \implies a = \frac{1}{b c}$$

*Make $a$ the subject.*

**LHS:**

$$\frac{1}{1 + a + b^{-1}} + \frac{1}{1 + b + c^{-1}} + \frac{1}{1 + c + a^{-1}}$$

$$= \frac{1}{b c + c + 1} + \frac{1}{b + 1 + \frac{1}{c}} + \frac{1}{1 + \frac{1}{b} + \frac{1}{b c}}$$

*Substitute $a = \frac{1}{b c}$.*

$$= \frac{b c}{b c + c + 1} + \frac{c}{b c + c + 1} + \frac{1}{b c + c + 1}$$

*Simplify each fraction.*

$$= \frac{b c + c + 1}{b c + c + 1}$$

*Add the fractions over their common denominator.*

$$= 1$$

*Cancel.*

This is the RHS, so LHS = RHS. Hence proved.

Valid where $b \neq 0$, $a + 1 + \frac{1}{b} \neq 0$, $c \neq 0$, $b + 1 + \frac{1}{c} \neq 0$, $a \neq 0$, $c + 1 + \frac{1}{a} \neq 0$.

## PD-MATH-IX-019

(c) If the medians of a triangles ABC intersect at G. Prove that area of $\Delta BCG = \frac{1}{3}$ area of $\Delta ABC$.

**Solution**

Take coordinates: $B = \left(0, 0\right)$, $C = \left(c, 0\right)$, $A = \left(p, q\right)$, $D = \left(\frac{c}{2}, 0\right)$, $E = \left(\frac{c}{2} + \frac{p}{2}, \frac{q}{2}\right)$, $G = \left(\frac{c}{3} + \frac{p}{3}, \frac{q}{3}\right)$.

*B at the origin, BC along the x-axis, A above it. G lies on the medians AD and BE (checked). Areas are by the coordinate formula; both triangles run the same way round, so the signed areas are the areas.*

These coordinates give: D is the midpoint of BC; E is the midpoint of CA; G lies on line AD; G lies on line BE.

Then:

$$\operatorname{ar}\left(\triangle ABC\right) = \frac{1}{2}\left[\left(0 - p\right)\left(0 - q\right) - \left(0 - q\right)\left(c - p\right)\right] = \frac{c q}{2}$$

$$\operatorname{ar}\left(\triangle BCG\right) = \frac{1}{2}\left[\left(c\right)\left(\frac{q}{3}\right) - \left(0\right)\left(\frac{c}{3} + \frac{p}{3}\right)\right] = \frac{c q}{6}$$

**LHS:**

$$\operatorname{ar}\left(\triangle BCG\right)$$

$$= \frac{c q}{6}$$

*Write each length, area or product in coordinates (see above).*

**RHS:**

$$\frac{\operatorname{ar}\left(\triangle ABC\right)}{3}$$

$$= \frac{p q}{6} + \frac{q \left(c - p\right)}{6}$$

*Write each length, area or product in coordinates (see above).*

$$= \frac{c q}{6}$$

*Simplify algebraically.*

Both sides reduce to the same expression, so LHS = RHS. Hence proved.

## PD-MATH-IX-020

b. Prove that: $$\frac{1}{\sqrt{2}+1} + \frac{1}{\sqrt{3}+\sqrt{2}} + \frac{1}{2+\sqrt{3}} = 1$$ (3)

**Solution**

**LHS:**

$$\frac{1}{\sqrt{2} + 1} + \frac{1}{\sqrt{3} + \sqrt{2}} + \frac{1}{2 + \sqrt{3}}$$

$$= \left(2 - \sqrt{3}\right) - \left(- \sqrt{3} + \sqrt{2}\right) - \left(1 - \sqrt{2}\right)$$

*Rationalise each denominator.*

$$= 1$$

*Cancel.*

This is the RHS, so LHS = RHS. Hence proved.

## PD-MATH-IX-024

X. (a) If O is any point in the interior of a rectangle ABCD. Prove that \( \mathrm{OA}^2 + \mathrm{OC}^2 = \mathrm{OB}^2 + \mathrm{OD}^2 \) [5]

**Solution**

Take coordinates: $A = \left(0, 0\right)$, $B = \left(a, 0\right)$, $C = \left(a, b\right)$, $D = \left(0, b\right)$, $O = \left(x, y\right)$.

*A at the origin, AB along the x-axis and AD along the y-axis; O = (x, y). The identity holds for any O.*

These coordinates give: ∠DAB = 90°; ∠ABC = 90°; ∠BCD = 90°; AB = DC.

Then:

$$OA^{2} = \left(0 - x\right)^{2} + \left(0 - y\right)^{2} = x^{2} + y^{2}$$

$$OB^{2} = \left(a - x\right)^{2} + \left(0 - y\right)^{2} = a^{2} - 2 a x + x^{2} + y^{2}$$

$$OC^{2} = \left(a - x\right)^{2} + \left(b - y\right)^{2} = a^{2} - 2 a x + b^{2} - 2 b y + x^{2} + y^{2}$$

$$OD^{2} = \left(0 - x\right)^{2} + \left(b - y\right)^{2} = b^{2} - 2 b y + x^{2} + y^{2}$$

**LHS:**

$$OA^{2} + OC^{2}$$

$$= x^{2} + y^{2} + \left(a - x\right)^{2} + \left(b - y\right)^{2}$$

*Write each length, area or product in coordinates (see above).*

**RHS:**

$$OB^{2} + OD^{2}$$

$$= x^{2} + y^{2} + \left(a - x\right)^{2} + \left(b - y\right)^{2}$$

*Write each length, area or product in coordinates (see above).*

Both sides reduce to the same expression, so LHS = RHS. Hence proved.

## PD-MATH-IX-025

(ii) Prove that the line segment joining the mid-points of the diagonals of a trapezium is parallel to the parallel sides of trapezium and is equal to half the difference of these sides.

**Solution**

**Part 1: $\overrightarrow{MN} \times \overrightarrow{AB} = 0$**

Take coordinates: $A = \left(0, 0\right)$, $B = \left(2 a, 0\right)$, $D = \left(2 d, 2 h\right)$, $C = \left(2 c + 2 d, 2 h\right)$, $M = \left(c + d, h\right)$, $N = \left(a + d, h\right)$.

*AB ∥ DC with AB = 2a, DC = 2c. M, N are the midpoints of the diagonals AC, BD. A zero cross product means MN ∥ AB; MN² = ((AB - DC)/2)² gives MN = half the difference.*

These coordinates give: AB ∥ DC; M is the midpoint of AC; N is the midpoint of BD.

Then:

$$\overrightarrow{MN} \times \overrightarrow{AB} = \left(a + d - \left(c + d\right)\right)\left(0\right) - \left(h - h\right)\left(2 a\right) = 0$$

**LHS:**

$$\overrightarrow{MN} \times \overrightarrow{AB}$$

$$= 0$$

*Write each length, area or product in coordinates (see above).*

This is the RHS, so LHS = RHS. Hence proved.

**Part 2: $MN^{2} = \left(\frac{AB - DC}{2}\right)^{2}$**

Take coordinates: $A = \left(0, 0\right)$, $B = \left(2 a, 0\right)$, $D = \left(2 d, 2 h\right)$, $C = \left(2 c + 2 d, 2 h\right)$, $M = \left(c + d, h\right)$, $N = \left(a + d, h\right)$.

*AB ∥ DC with AB = 2a, DC = 2c. M, N are the midpoints of the diagonals AC, BD. A zero cross product means MN ∥ AB; MN² = ((AB - DC)/2)² gives MN = half the difference.*

These coordinates give: AB ∥ DC; M is the midpoint of AC; N is the midpoint of BD.

Then:

$$AB = \sqrt{\left(2 a\right)^{2} + \left(0\right)^{2}} = 2 a$$

$$DC = \sqrt{\left(2 c + 2 d - 2 d\right)^{2} + \left(2 h - 2 h\right)^{2}} = 2 c$$

$$MN^{2} = \left(a + d - \left(c + d\right)\right)^{2} + \left(h - h\right)^{2} = \left(a - c\right)^{2}$$

From the earlier part: $\overrightarrow{MN} \times \overrightarrow{AB} = 0$.

**LHS:**

$$MN^{2}$$

$$= \left(a - c\right)^{2}$$

*Write each length, area or product in coordinates (see above).*

**RHS:**

$$\left(\frac{AB - DC}{2}\right)^{2}$$

$$= \left(a - c\right)^{2}$$

*Write each length, area or product in coordinates (see above).*

Both sides reduce to the same expression, so LHS = RHS. Hence proved.

## PD-MATH-X-001

3. a) Prove the following Identity:

$$(\sin A + \text{cosec } A)^2 + (\cos A + \text{sec } A)^2 = 5 + \text{sec}^2 A \text{ cosec}^2 A \tag{3}$$

**Solution**

**LHS:**

$$\left(\sin A + \operatorname{cosec} A\right)^{2} + \left(\cos A + \sec A\right)^{2}$$

$$= \left(\sin A + \frac{1}{\sin A}\right)^{2} + \left(\cos A + \frac{1}{\cos A}\right)^{2}$$

*Use the reciprocal and quotient identities.*

$$= \sin^{2} A + \cos^{2} A + 4 + \frac{1}{\cos^{2} A} + \frac{1}{\sin^{2} A}$$

*Expand algebraically.*

$$= 5 + \frac{1}{\cos^{2} A} + \frac{1}{\sin^{2} A}$$

*Use sin² A + cos² A = 1.*

$$= \left(\tan^{2} A + 1\right) \operatorname{cosec}^{2} A + 5$$

*Use the reciprocal and quotient identities and simplify.*

**RHS:**

$$5 + \sec^{2} A \operatorname{cosec}^{2} A$$

$$= \left(\tan^{2} A + 1\right) \operatorname{cosec}^{2} A + 5$$

*Use sec² A = 1 + tan² A.*

Both sides reduce to the same expression, so LHS = RHS. Hence proved.

Valid where $\sin A \neq 0$, $\cos A \neq 0$.

## PD-MATH-X-002

a) Prove that : sec⁴A(1 - sin⁴A) - 2tan²A = 1 (3)

**Solution**

**LHS:**

$$\sec^{4} A \left(1 - \sin^{4} A\right) - 2 \tan^{2} A$$

$$= \frac{1 - \sin^{4} A}{\cos^{4} A} - \frac{2 \sin^{2} A}{\cos^{2} A}$$

*Use the reciprocal and quotient identities.*

$$= \frac{1 - \left(1 - \cos^{2} A\right)^{2}}{\cos^{4} A} - \frac{2 \left(1 - \cos^{2} A\right)}{\cos^{2} A}$$

*Use sin² A = 1 - cos² A in the even powers.*

$$= \frac{2 - \cos^{2} A}{\cos^{2} A} + \frac{2 \cos^{2} A - 2}{\cos^{2} A}$$

*Simplify each fraction.*

$$= \frac{\left(2 - \cos^{2} A\right) + \left(2 \cos^{2} A - 2\right)}{\cos^{2} A}$$

*Add the fractions over their common denominator.*

$$= 1$$

*Cancel.*

This is the RHS, so LHS = RHS. Hence proved.

Valid where $\cos A \neq 0$.

## PD-MATH-X-003

b) If x, y, z are in continued proportion, prove that:

$$\frac{(x+y)^2}{(y+z)^2} = \frac{x}{z} \tag{3}$$

**Solution**

Since the terms are in GP (the square of the middle term is the product of the others): $y^{2} = x z$.

**LHS:**

$$\frac{\left(x + y\right)^{2}}{\left(y + z\right)^{2}}$$

$$= \frac{x^{2} + 2 x y + y^{2}}{y^{2} + 2 y z + z^{2}}$$

*Expand the numerator and the denominator.*

$$= \frac{x^{2} + 2 x y + x z}{x z + 2 y z + z^{2}}$$

*Use the given $y^{2} = x z$.*

$$= \frac{x \left(x + 2 y + z\right)}{z \left(x + 2 y + z\right)}$$

*Factorise the numerator and the denominator.*

$$= \frac{x}{z}$$

*Cancel the common factor.*

This is the RHS, so LHS = RHS. Hence proved.

Valid where $y + z \neq 0$, $z \neq 0$, $x \neq 0$, $y \neq 0$.

## PD-MATH-X-004

(iii) Prove that : \(\sec^2 A\). cosec\(^2\) \(A = \tan^2 A + \cot^2 A + 2\) [4]

**Solution**

**LHS:**

$$\sec^{2} A \operatorname{cosec}^{2} A$$

$$= \left(\tan^{2} A + 1\right) \operatorname{cosec}^{2} A$$

*Use sec² A = 1 + tan² A.*

$$= \left(\tan^{2} A + 1\right) \left(\cot^{2} A + 1\right)$$

*Use cosec² A = 1 + cot² A.*

$$= \tan^{2} A + \cot^{2} A + 2$$

*Use the reciprocal and quotient identities and simplify.*

This is the RHS, so LHS = RHS. Hence proved.

Valid where $\cos A \neq 0$, $\sin A \neq 0$.

## PD-MATH-X-005

(ii) Prove that: \(\frac{1 + \sin\theta}{1 - \sin\theta} -\frac{1 - \sin\theta}{1 + \sin\theta} = 4\tan \theta \sec \theta\) [3]

**Solution**

**LHS:**

$$\frac{1 + \sin A}{1 - \sin A} - \frac{1 - \sin A}{1 + \sin A}$$

$$= \frac{- \sin A - 1}{\sin A - 1} + \frac{\sin A - 1}{\sin A + 1}$$

*Simplify each fraction.*

$$= \frac{\left(- \sin A - 1\right) \left(\sin A + 1\right) + \left(\sin A - 1\right)^{2}}{\left(\sin A - 1\right) \left(\sin A + 1\right)}$$

*Take a common denominator.*

$$= \frac{\left(-1\right) 4 \sin A}{\left(\sin A - 1\right) \left(\sin A + 1\right)}$$

*Expand the numerator.*

$$= - \frac{4 \sin A}{\left(\sin A - 1\right) \left(\sin A + 1\right)}$$

*Factorise.*

$$= \frac{4 \sin A}{1 - \sin^{2} A}$$

*Simplify.*

**RHS:**

$$4 \tan A \sec A$$

$$= \frac{4 \sin A}{\cos^{2} A}$$

*Use the reciprocal and quotient identities.*

$$= \frac{4 \sin A}{1 - \sin^{2} A}$$

*Use cos² A = 1 - sin² A in the even powers.*

Both sides reduce to the same expression, so LHS = RHS. Hence proved.

Valid where $1 - \sin A \neq 0$, $\sin A + 1 \neq 0$, $\cos A \neq 0$.

## PD-MATH-X-006

(i) If \((a^2 + b^2)(x^2 + y^2) = (ax + by)^2\); Prove that \(\frac{x}{y} = \frac{a}{b}\) [3]

**Solution**

Given: $\left(a^{2} + b^{2}\right) \left(x^{2} + y^{2}\right) = \left(a x + b y\right)^{2}$.

From the given condition:

$$\left(a^{2} + b^{2}\right) \left(x^{2} + y^{2}\right) = \left(a x + b y\right)^{2} \implies a^{2} y^{2} - 2 a b x y + b^{2} x^{2} = 0$$

*Bring every term to one side and expand.*

$$a^{2} y^{2} - 2 a b x y + b^{2} x^{2} = 0 \implies \left(- a y + b x\right)^{2} = 0$$

*Factorise.*

$$\left(- a y + b x\right)^{2} = 0 \implies - a y + b x = 0$$

*A product is zero only if a factor is zero, and the other factors are nonzero, so $- a y + b x = 0$.*

$$- a y + b x = 0 \implies x = \frac{a y}{b}$$

*Make $x$ the subject.*

**LHS:**

$$\frac{x}{y}$$

$$= \frac{a}{b}$$

*Substitute $x = \frac{a y}{b}$.*

This is the RHS, so LHS = RHS. Hence proved.

Valid where $y \neq 0$, $b \neq 0$.

## PD-MATH-X-007

(i) Using factor theorem show that \( (3x + 2) \) is a factor of \( 3x^{3} + 2x^{2} - 3x - 2 \) . Hence, factorise the expression \( 3x^{3} + 2x^{2} - 3x - 2 \) completely. [3]

**Solution**

Let $P(x) = 3 x^{3} + 2 x^{2} - 3 x - 2$. The factor $3 x + 2$ is zero at $x = - \frac{2}{3}$.

$$P\left(- \frac{2}{3}\right) = -2 - 3 \left(- \frac{2}{3}\right) + 2 \left(- \frac{2}{3}\right)^{2} + 3 \left(- \frac{2}{3}\right)^{3} = 0$$

By the factor theorem, $3 x + 2$ is a factor of $P(x)$.

*Divide by $3 x + 2$.*

$$3 x^{3} + 2 x^{2} - 3 x - 2 = \left(3 x + 2\right) \left(x^{2} - 1\right)$$

*Combine and factor the algebraic expression.*

$$\left(3 x + 2\right) \left(x^{2} - 1\right) = \left(x - 1\right) \left(x + 1\right) \left(3 x + 2\right)$$

The last line is the complete factorisation.

## PD-MATH-X-009

b) Given x = $$\frac{\sqrt{a^2 + b^2} + \sqrt{a^2 - b^2}}{\sqrt{a^2 + b^2} - \sqrt{a^2 - b^2}}$$.

Use componendo and dividendo to prove that $$b^2 = \frac{2a^2x}{x^2 + 1}$$. [3]

**Solution**

Given: $x = \frac{\sqrt{a^{2} + b^{2}} + \sqrt{a^{2} - b^{2}}}{\sqrt{a^{2} + b^{2}} - \sqrt{a^{2} - b^{2}}}$.

$$\implies \frac{x + 1}{x - 1} = \frac{\sqrt{a^{2} + b^{2}}}{\sqrt{a^{2} - b^{2}}}$$

*Componendo and dividendo: if $\frac{a}{b} = \frac{c}{d}$ then $\frac{a + b}{a - b} = \frac{c + d}{c - d}$.*

$$\implies \frac{\left(x + 1\right)^{2}}{\left(x - 1\right)^{2}} = \frac{a^{2} + b^{2}}{a^{2} - b^{2}}$$

*Square both sides.*

$$\implies \frac{\left(x + 1\right)^{2}}{\left(x - 1\right)^{2}} = \frac{a^{2} + b^{2}}{\left(a - b\right) \left(a + b\right)}$$

*Simplify each side.*

$$\implies \frac{x^{2} + 1}{2 x} = \frac{a^{2} + b^{2} + \left(a - b\right) \left(a + b\right)}{a^{2} + b^{2} - \left(a - b\right) \left(a + b\right)}$$

*Componendo and dividendo: if $\frac{a}{b} = \frac{c}{d}$ then $\frac{a + b}{a - b} = \frac{c + d}{c - d}$.*

$$\implies \frac{x^{2} + 1}{2 x} = \frac{a^{2}}{b^{2}}$$

*Simplify each side.*

$$\implies b^{2} \left(x^{2} + 1\right) = 2 a^{2} x$$

*Cross-multiply to clear the denominators.*

$$\implies b^{2} = \frac{2 a^{2} x}{x^{2} + 1}$$

*Make $b^{2}$ the subject.*

Hence proved.

Valid where $a^{2} - b^{2} \geq 0$, $- \sqrt{a^{2} - b^{2}} + \sqrt{a^{2} + b^{2}} \neq 0$.

## PD-MATH-X-010

a) If $$\frac{3p + 4q}{3r + 4s} = \frac{3p - 4q}{3r - 4s}$$, Prove that $$\frac{p}{q} = \frac{r}{s}$$ [3]

**Solution**

Given: $\frac{3 p + 4 q}{3 r + 4 s} = \frac{3 p - 4 q}{3 r - 4 s}$.

From the given condition:

$$\frac{3 p + 4 q}{3 r + 4 s} = \frac{3 p - 4 q}{3 r - 4 s} \implies p = \frac{q r}{s}$$

*Make $p$ the subject.*

**LHS:**

$$\frac{p}{q}$$

$$= \frac{r}{s}$$

*Substitute $p = \frac{q r}{s}$.*

This is the RHS, so LHS = RHS. Hence proved.

Valid where $q \neq 0$, $s \neq 0$, $3 r + 4 s \neq 0$, $3 r - 4 s \neq 0$.

## PD-MATH-X-011

- b) A solid sphere and hemisphere have the same total surface area. Prove that the ratio of their volume is $$\frac{3\sqrt{3}}{4}$$

**Solution**

Given: $4 \pi r^{2} = 3 \pi R^{2}$.

From the given condition:

$$4 \pi r^{2} = 3 \pi R^{2} \implies R^{2} = \frac{4 r^{2}}{3}$$

*Make $R^{2}$ the subject.*

$$R^{2} = \frac{4 r^{2}}{3} \implies R = \frac{2 \sqrt{3} r}{3}$$

*Take the positive root, since $R > 0$.*

**LHS:**

$$\frac{\frac{4 \pi r^{3}}{3}}{\frac{2 \pi R^{3}}{3}}$$

$$= \frac{2 r^{3}}{R^{3}}$$

*Simplify.*

$$= \frac{3 \sqrt{3}}{4}$$

*Substitute $R = \frac{2 \sqrt{3} r}{3}$.*

This is the RHS, so LHS = RHS. Hence proved.

Valid where $R \neq 0$.

## PD-MATH-X-015

a) If the equation \((1 + \mathrm{m}^2)\mathrm{x}^2 + 2\mathrm{mcx} + \mathrm{c}^2 - \mathrm{a}^2 = 0\) has equal roots, show that \(c^2 = a^2(1 + m^2)\)

**Solution**

Equal roots means the discriminant $b^2 - 4ac$ is zero: $4 c^{2} m^{2} - \left(- a^{2} + c^{2}\right) \left(4 m^{2} + 4\right) = 0$.

From the given condition:

$$4 c^{2} m^{2} - \left(- a^{2} + c^{2}\right) \left(4 m^{2} + 4\right) = 0 \implies c^{2} = a^{2} \left(m^{2} + 1\right)$$

*Make $c^{2}$ the subject.*

**LHS:**

$$c^{2}$$

$$= a^{2} \left(m^{2} + 1\right)$$

*Substitute $c^{2} = a^{2} \left(m^{2} + 1\right)$.*

This is the RHS, so LHS = RHS. Hence proved.

## PD-MATH-X-017

32. (A) If a line is drawn parallel to one side of a triangle to intersect the other two sides in distinct points, then prove that other two sides are divided in the same ratio. 5

**Solution**

Take coordinates: $B = \left(0, 0\right)$, $C = \left(c, 0\right)$, $A = \left(p, q\right)$, $D = \left(- p t + p, - q t + q\right)$, $E = \left(p + u \left(c - p\right), - q u + q\right)$.

*D = A + t(B - A) and E = A + u(C - A). AD/DB = AE/EC is shown as AD²·EC² = AE²·DB² (lengths are positive).*

These coordinates give: D lies on line AB; E lies on line AC.

Then:

$$\overrightarrow{DE} \times \overrightarrow{BC} = \left(p + u \left(c - p\right) - \left(- p t + p\right)\right)\left(0\right) - \left(- q u + q - \left(- q t + q\right)\right)\left(c\right) = - c q \left(t - u\right)$$

$$AD^{2} = \left(- p t + p - p\right)^{2} + \left(- q t + q - q\right)^{2} = t^{2} \left(p^{2} + q^{2}\right)$$

$$AE^{2} = \left(p + u \left(c - p\right) - p\right)^{2} + \left(- q u + q - q\right)^{2} = u^{2} \left(c^{2} - 2 c p + p^{2} + q^{2}\right)$$

$$DB^{2} = \left(0 - \left(- p t + p\right)\right)^{2} + \left(0 - \left(- q t + q\right)\right)^{2} = \left(p^{2} + q^{2}\right) \left(t - 1\right)^{2}$$

$$EC^{2} = \left(c - \left(p + u \left(c - p\right)\right)\right)^{2} + \left(0 - \left(- q u + q\right)\right)^{2} = \left(u - 1\right)^{2} \left(c^{2} - 2 c p + p^{2} + q^{2}\right)$$

Given: $\overrightarrow{DE} \times \overrightarrow{BC} = 0$.

From the given condition:

$$\overrightarrow{DE} \times \overrightarrow{BC} = 0 \implies - c \left(q t - q u\right) = 0$$

*Write each length, area or product in coordinates (see above).*

$$- c \left(q t - q u\right) = 0 \implies t = u$$

*Make $t$ the subject.*

**LHS:**

$$AD^{2} EC^{2}$$

$$= \left(p^{2} t^{2} + q^{2} t^{2}\right) \left(\left(q u - q\right)^{2} + \left(c - p - u \left(c - p\right)\right)^{2}\right)$$

*Write each length, area or product in coordinates (see above).*

$$= \left(p^{2} u^{2} + q^{2} u^{2}\right) \left(\left(q u - q\right)^{2} + \left(c - p - u \left(c - p\right)\right)^{2}\right)$$

*Substitute $t = u$.*

$$= \left(q^{2} u^{2} + u^{2} \left(c - p\right)^{2}\right) \left(\left(p u - p\right)^{2} + \left(q u - q\right)^{2}\right)$$

*Simplify.*

**RHS:**

$$AE^{2} DB^{2}$$

$$= \left(q^{2} u^{2} + u^{2} \left(c - p\right)^{2}\right) \left(\left(p t - p\right)^{2} + \left(q t - q\right)^{2}\right)$$

*Write each length, area or product in coordinates (see above).*

$$= \left(q^{2} u^{2} + u^{2} \left(c - p\right)^{2}\right) \left(\left(p u - p\right)^{2} + \left(q u - q\right)^{2}\right)$$

*Substitute $t = u$.*

Both sides reduce to the same expression, so LHS = RHS. Hence proved.

## PD-MATH-X-021

7. एक समांतर श्रेढ़ी का चौथा पद शून्य है। सिद्ध कीजिए कि इसका 25 वां पद, उसके 11 वें पद का तीन गुना है।

The 4$^{th}$ term of an A.P. is zero. Prove that the 25$^{th}$ term of the A.P. is three times its 11$^{th}$ term.

**Solution**

Given: $T_{4} = 0$.

Let T be the AP with first term $a$ and common difference $d$.

From the given condition:

$$T_{4} = 0 \implies a + 3 d = 0$$

*Use the general term $T_k = a + (k-1)d$.*

$$a + 3 d = 0 \implies a = - 3 d$$

*Make $a$ the subject.*

**LHS:**

$$T_{25}$$

$$= a + 24 d$$

*Use the general term $T_k = a + (k-1)d$.*

$$= 21 d$$

*Substitute $a = - 3 d$.*

**RHS:**

$$3 T_{11}$$

$$= 3 a + 30 d$$

*Use the general term $T_k = a + (k-1)d$.*

$$= 21 d$$

*Substitute $a = - 3 d$.*

Both sides reduce to the same expression, so LHS = RHS. Hence proved.

## PD-MATH-X-022

20. तीन समांतर श्रेणियों के प्रथम $n$ पदों का योग क्रमशः $S_1, S_2$ तथा $S_3$ हैं। तीनों का प्रथम पद 1 है तथा सार्व अन्तर क्रमशः 1, 2 तथा 3 हैं। सिद्ध कीजिए कि $S_1 + S_3 = 2S_2$ .

The sums of first $n$ terms of three arithmetic progressions are $S_1, S_2$ and $S_3$ respectively. The first term of each A.P. is 1 and their common differences are 1, 2 and 3 respectively. Prove that $S_1 + S_3 = 2S_2$ .

**Solution**

Let P be the AP with first term $1$ and common difference $1$.

Let Q be the AP with first term $1$ and common difference $2$.

Let R be the AP with first term $1$ and common difference $3$.

**LHS:**

$$S_1 + S_3$$

$$= \frac{n \left(n + 1\right)}{2} + \frac{n \left(3 n - 1\right)}{2}$$

*Use $S_n = \frac{n}{2}[2a + (n-1)d]$.*

$$= \left(\frac{n^{2}}{2} + \frac{n}{2}\right) + \left(\frac{3 n^{2}}{2} - \frac{n}{2}\right)$$

*Expand.*

$$= 2 n^{2}$$

*Collect like terms.*

**RHS:**

$$2 S_2$$

$$= 2 n^{2}$$

*Use $S_n = \frac{n}{2}[2a + (n-1)d]$.*

Both sides reduce to the same expression, so LHS = RHS. Hence proved.

## PD-MATH-X-023

22. एक सीधी रेखा में स्थित घरों पर 1 से 49 तक की संख्याएँ (क्रमानुसार) अंकित हैं। दर्शाइए कि इन अंकित संख्याओं में एक ऐसी संख्या X अवश्य है कि X से पहले आने वाले घरों पर की अंकित संख्याओं का योग, X के बाद आनेवाली अंकित संख्याओं के योग के बराबर है। The houses in a row are numbered consecutively from 1 to 49. Show that there exists a value of X such that sum of numbers of houses proceeding the house numbered X is equal to sum of the numbers of houses following X.

**Solution**

Let N be the AP with first term $1$ and common difference $1$.

The condition on $X$ is:

$$S_{X - 1} = S_{49} - S_{X}$$

$$\iff \frac{X \left(X - 1\right)}{2} = - \frac{X \left(X + 1\right)}{2} + 1225$$

*Use $S_n = \frac{n}{2}[2a + (n-1)d]$.*

$$\iff X^{2} - 1225 = 0$$

*Bring every term to one side and expand.*

$$\iff \left(X - 35\right) \left(X + 35\right) = 0$$

*Factorise.*

$$X = 35$$

*Keep the root that satisfies the conditions; reject -35.*

This value lies between $1$ and $49$, so the required $X$ exists.

## PD-MATH-X-025

Prove that the lengths of tangents drawn from an external point to a circle are equal.

**Solution**

Take coordinates: $O = \left(0, 0\right)$, $P = \left(p, 0\right)$, $T = \left(\frac{r^{2}}{p}, \frac{r \sqrt{p^{2} - r^{2}}}{p}\right)$, $U = \left(\frac{r^{2}}{p}, - \frac{r \sqrt{p^{2} - r^{2}}}{p}\right)$.

*Centre O at the origin and the external point P = (p, 0), p > r. T and U are the points of contact: OT = OU = r and OT ⊥ PT, OU ⊥ PU (checked). Equal squared lengths give PT = PU.*

These coordinates give: OT = OU; ∠OTP = 90°; ∠OUP = 90°.

Then:

$$PT^{2} = \left(\frac{r^{2}}{p} - p\right)^{2} + \left(\frac{r \sqrt{p^{2} - r^{2}}}{p}\right)^{2} = \left(p - r\right) \left(p + r\right)$$

$$PU^{2} = \left(\frac{r^{2}}{p} - p\right)^{2} + \left(- \frac{r \sqrt{p^{2} - r^{2}}}{p}\right)^{2} = \left(p - r\right) \left(p + r\right)$$

**LHS:**

$$PT^{2}$$

$$= \left(- p + \frac{r^{2}}{p}\right)^{2} + \frac{r^{2} \left(p^{2} - r^{2}\right)}{p^{2}}$$

*Write each length, area or product in coordinates (see above).*

**RHS:**

$$PU^{2}$$

$$= \left(- p + \frac{r^{2}}{p}\right)^{2} + \frac{r^{2} \left(p^{2} - r^{2}\right)}{p^{2}}$$

*Write each length, area or product in coordinates (see above).*

Both sides reduce to the same expression, so LHS = RHS. Hence proved.

## PD-MATH-X-026

Prove that the area of an equilateral triangle described on one side of the square is equal to half the area of the equilateral triangle described on one of its diagonal.

**Solution**

Given: $d^{2} = 2 a^{2}$.

**LHS:**

$$\frac{\sqrt{3}}{4} a^{2}$$

**RHS:**

$$\frac{\frac{\sqrt{3}}{4} d^{2}}{2}$$

$$= \frac{\sqrt{3} a^{2}}{4}$$

*Use the given $d^{2} = 2 a^{2}$.*

Both sides reduce to the same expression, so LHS = RHS. Hence proved.

## PD-MATH-X-028

In an equilateral ΔABC, D is a point on side BC such that BD = 1/3 BC. Prove that 9(AD)^2 = 7(AB)^2

**Solution**

Take coordinates: $B = \left(0, 0\right)$, $C = \left(3 a, 0\right)$, $A = \left(\frac{3 a}{2}, \frac{3 \sqrt{3} a}{2}\right)$, $D = \left(a, 0\right)$.

*Side 3a with B at the origin and BC along the x-axis; D = (a, 0) gives BD = a = BC/3.*

These coordinates give: AB = BC; AC = BC; D lies on line BC.

Then:

$$AB^{2} = \left(0 - \frac{3 a}{2}\right)^{2} + \left(0 - \frac{3 \sqrt{3} a}{2}\right)^{2} = 9 a^{2}$$

$$AD^{2} = \left(a - \frac{3 a}{2}\right)^{2} + \left(0 - \frac{3 \sqrt{3} a}{2}\right)^{2} = 7 a^{2}$$

**LHS:**

$$9 AD^{2}$$

$$= 63 a^{2}$$

*Write each length, area or product in coordinates (see above).*

**RHS:**

$$7 AB^{2}$$

$$= 63 a^{2}$$

*Write each length, area or product in coordinates (see above).*

Both sides reduce to the same expression, so LHS = RHS. Hence proved.

## PD-MATH-X-030

9. पूर्ण वर्ग बनाने की विधि का प्रयोग करते हुए दर्शाइए कि समीकरण $$x^2 - 8x + 18 = 0$$ का कोई हल नहीं है।

Using completing the square method, show that the equation $$x^2 - 8x + 18 = 0$$ has no solution.

**Solution**

Complete the square:

$$x^{2} - 8 x + 18 = \left(x - 4\right)^{2} + 2$$

Since a square of a real number is nonnegative, $$\left(x - 4\right)^{2} + 2 > 0$$ for every real $x$.

Therefore the equation has no real solution.

## PD-MATH-XI-002

11. If $\tan A - \tan B = x$ and $\cot B - \cot A = y$, prove that: $\cot (A - B) = \frac{1}{x} + \frac{1}{y}$.

**Solution**

Given: $\tan A - \tan B = x$ and $\cot B - \cot A = y$.

**LHS:**

$$\cot\left(A - B\right)$$

$$= \frac{- \cot A \cot B - 1}{\cot A - \cot B}$$

*Use the compound-angle formula.*

$$= \frac{1}{- \cot A + \cot B} + \frac{1}{\tan A - \tan B}$$

*Use the reciprocal and quotient identities and simplify.*

**RHS:**

$$\frac{1}{x} + \frac{1}{y}$$

$$= \frac{1}{- \cot A + \cot B} + \frac{1}{\tan A - \tan B}$$

*Substitute $x = \tan A - \tan B$ and $y = - \cot A + \cot B$.*

Both sides reduce to the same expression, so LHS = RHS. Hence proved.

Valid where $\sin\left(A - B\right) \neq 0$, $x \neq 0$, $y \neq 0$, $\cos A \neq 0$, $\cos B \neq 0$, $\sin B \neq 0$, $\sin A \neq 0$.

## PD-MATH-XI-003

15. Prove that :

$$\cos 20^{\circ} \cos 40^{\circ} \cos 60^{\circ} \cos 80^{\circ}=\frac{1}{16}$$

**Solution**

**LHS:**

$$\cos 20^\circ \cos 40^\circ \cos 60^\circ \cos 80^\circ$$

$$= \frac{\cos 20^{\circ} \cos 40^{\circ} \cos 80^{\circ}}{2}$$

*Use the values of the trigonometric ratios of standard angles.*

$$= \frac{\left(\frac{\cos 20^{\circ}}{2} + \frac{1}{4}\right) \cos 80^{\circ}}{2}$$

*Use the product-to-sum formulae, e.g. $2\cos P\cos Q = \cos(P+Q) + \cos(P-Q)$.*

$$= \frac{\cos 20^{\circ} \cos 80^{\circ}}{4} + \frac{\cos 80^{\circ}}{8}$$

*Expand algebraically.*

$$= \frac{1}{16}$$

*Use the product-to-sum formulae, e.g. $2\cos P\cos Q = \cos(P+Q) + \cos(P-Q)$.*

This is the RHS, so LHS = RHS. Hence proved.

## PD-MATH-XI-004

16. If $\sin \alpha + \sin \beta = a$ and $\cos \alpha + \cos \beta = b$, prove that

i) $\cos(\alpha-\beta)=\frac{a^{2}+b^{2}-2}{2}$ [2½]

ii) $\tan\left(\frac{\alpha-\beta}{2}\right)=\pm\sqrt{\frac{4-a^{2}-b^{2}}{a^{2}+b^{2}}}$ [2½]

**Solution**

**Part 1: $\cos\left(\alpha - \beta\right) = \frac{a^{2} + b^{2} - 2}{2}$**

Given: $\sin \alpha + \sin \beta = a$ and $\cos \alpha + \cos \beta = b$.

**LHS:**

$$\cos\left(\alpha - \beta\right)$$

$$= \sin \alpha \sin \beta + \cos \alpha \cos \beta$$

*Use the compound-angle formula.*

**RHS:**

$$\frac{a^{2} + b^{2} - 2}{2}$$

$$= \frac{b^{2}}{2} + \frac{\left(\sin \alpha + \sin \beta\right)^{2}}{2} - 1$$

*Substitute $a = \sin \alpha + \sin \beta$.*

$$= \frac{b^{2}}{2} + \frac{\sin^{2} \alpha}{2} + \sin \alpha \sin \beta + \frac{\sin^{2} \beta}{2} - 1$$

*Expand algebraically.*

$$= \frac{b^{2}}{2} + \sin \alpha \sin \beta - \frac{\cos^{2} \alpha}{2} - \frac{\cos^{2} \beta}{2}$$

*Use sin² A = 1 - cos² A in the even powers.*

$$= \frac{\left(\cos \alpha + \cos \beta\right)^{2}}{2} + \sin \alpha \sin \beta - \frac{\cos^{2} \alpha}{2} - \frac{\cos^{2} \beta}{2}$$

*Substitute $b = \cos \alpha + \cos \beta$.*

$$= \left(\frac{\cos^{2} \alpha}{2} + \cos \alpha \cos \beta + \frac{\cos^{2} \beta}{2}\right) + \sin \alpha \sin \beta - \frac{\cos^{2} \alpha}{2} - \frac{\cos^{2} \beta}{2}$$

*Expand.*

$$= \sin \alpha \sin \beta + \cos \alpha \cos \beta$$

*Collect like terms.*

Both sides reduce to the same expression, so LHS = RHS. Hence proved.

**Part 2: $\tan^{2}\left(\frac{\alpha - \beta}{2}\right) = \frac{4 - a^{2} - b^{2}}{a^{2} + b^{2}}$**

Given: $\sin \alpha + \sin \beta = a$ and $\cos \alpha + \cos \beta = b$.

From the earlier part: $\cos\left(\alpha - \beta\right) = \frac{a^{2}}{2} + \frac{b^{2}}{2} - 1$.

**LHS:**

$$\tan^{2}\left(\frac{\alpha - \beta}{2}\right)$$

$$= \frac{1 - \cos\left(\alpha - \beta\right)}{\cos\left(\alpha - \beta\right) + 1}$$

*Use $\tan^2\theta = \frac{1 - \cos 2\theta}{1 + \cos 2\theta}$.*

$$= \frac{- \frac{a^{2}}{2} - \frac{b^{2}}{2} + 2}{\frac{a^{2}}{2} + \frac{b^{2}}{2}}$$

*Use the given $\cos\left(\alpha - \beta\right) = \frac{a^{2}}{2} + \frac{b^{2}}{2} - 1$.*

$$= \frac{- a^{2} - b^{2} + 4}{a^{2} + b^{2}}$$

*Multiply the numerator and the denominator by 2.*

This is the RHS, so LHS = RHS. Hence proved.

Valid where $\cos\left(\frac{\alpha}{2} - \frac{\beta}{2}\right) \neq 0$, $a^{2} + b^{2} \neq 0$.

## PD-MATH-XI-005

23. If $a^2, b^2, c^2$ are in A.P., prove that $\frac{1}{b + c}, \frac{1}{c + a}, \frac{1}{a + b}$ are in A.P.

**Solution**

Since the terms are in AP (twice the middle term is the sum of the others): $2 b^{2} = a^{2} + c^{2}$.

**LHS − RHS:**

$$- \frac{1}{b + c} + \frac{2}{a + c} - \frac{1}{a + b}$$

$$= \frac{- \left(a + b\right) \left(a + c\right) + 2 \left(a + b\right) \left(b + c\right) - \left(a + c\right) \left(b + c\right)}{\left(a + b\right) \left(a + c\right) \left(b + c\right)}$$

*Take a common denominator.*

$$= \frac{- a^{2} + 2 b^{2} - c^{2}}{\left(a + b\right) \left(a + c\right) \left(b + c\right)}$$

*Expand the numerator.*

$$= 0$$

*Use the given $2 b^{2} = a^{2} + c^{2}$.*

Since LHS − RHS = 0, LHS = RHS. Hence proved.

Valid where $b + c \neq 0$, $a + c \neq 0$, $a + b \neq 0$.

## PD-MATH-XI-006

28. If A and G be the AM and GM between two positive numbers, then prove that the numbers are $A \pm \sqrt{A^2 - G^2}$

**Solution**

**Part 1: $b + d = \frac{b + d + b}{2} + \sqrt{\left(\frac{b + d + b}{2}\right)^{2} - \left(b + d\right) b}$**

**LHS:**

$$b + d$$

**RHS:**

$$\frac{b + d + b}{2} + \sqrt{\left(\frac{b + d + b}{2}\right)^{2} - \left(b + d\right) b}$$

$$= b + d$$

*Simplify under the root sign (a square root of a square of a nonnegative quantity is that quantity).*

Both sides reduce to the same expression, so LHS = RHS. Hence proved.

Valid where $- b \left(b + d\right) + \left(b + \frac{d}{2}\right)^{2} \geq 0$.

**Part 2: $b = \frac{b + d + b}{2} - \sqrt{\left(\frac{b + d + b}{2}\right)^{2} - \left(b + d\right) b}$**

From the earlier part: $b + d = b + \frac{d}{2} + \sqrt{- b \left(b + d\right) + \left(b + \frac{d}{2}\right)^{2}}$.

**LHS:**

$$b$$

**RHS:**

$$\frac{b + d + b}{2} - \sqrt{\left(\frac{b + d + b}{2}\right)^{2} - \left(b + d\right) b}$$

$$= b$$

*Simplify under the root sign (a square root of a square of a nonnegative quantity is that quantity).*

Both sides reduce to the same expression, so LHS = RHS. Hence proved.

Valid where $- b \left(b + d\right) + \left(b + \frac{d}{2}\right)^{2} \geq 0$.

## PD-MATH-XI-009

32. i) If a² + b², ab + bc and b² + c² are in G.P., prove that a, b, c are also in GP [2]

**Solution**

Since the terms are in GP (the square of the middle term is the product of the others): $\left(a b + b c\right)^{2} = \left(a^{2} + b^{2}\right) \left(b^{2} + c^{2}\right)$.

From the given condition:

$$\left(a b + b c\right)^{2} = \left(a^{2} + b^{2}\right) \left(b^{2} + c^{2}\right) \implies - a^{2} c^{2} + 2 a b^{2} c - b^{4} = 0$$

*Bring every term to one side and expand.*

$$- a^{2} c^{2} + 2 a b^{2} c - b^{4} = 0 \implies - \left(a c - b^{2}\right)^{2} = 0$$

*Factorise.*

$$- \left(a c - b^{2}\right)^{2} = 0 \implies a c - b^{2} = 0$$

*A product is zero only if a factor is zero, and the other factors are nonzero, so $a c - b^{2} = 0$.*

**LHS:**

$$b^{2}$$

$$= a c$$

*Substitute $b^{2} = a c$.*

This is the RHS, so LHS = RHS. Hence proved.

Valid where $a \neq 0$, $b \neq 0$, $c \neq 0$.

## PD-MATH-XI-010

ii) Prove that : sin x/cos 3x + sin 3x/cos 9x + sin 9x/cos 27x = 1/2 (tan 27x - tanx) [3]

**Solution**

**LHS:**

$$\frac{\sin x}{\cos 3x} + \frac{\sin 3x}{\cos 9x} + \frac{\sin 9x}{\cos 27x}$$

$$= \frac{\sin x \cos x}{\cos x \cos 3x} + \frac{\sin 3x \cos 3x}{\cos 3x \cos 9x} + \frac{\sin 9x \cos 9x}{\cos 9x \cos 27x}$$

*Multiply the numerator and denominator by $\cos$ of the numerator's angle.*

$$= \frac{\sin 2x}{2 \cos x \cos 3x} + \frac{\sin 6x}{2 \cos 3x \cos 9x} + \frac{\sin 18x}{2 \cos 9x \cos 27x}$$

*Use $2\sin A\cos A = \sin 2A$.*

$$= - \frac{\tan x}{2} + \frac{\tan 27x}{2}$$

*Use $\frac{\sin(P-Q)}{\cos P\cos Q} = \tan P - \tan Q$.*

This is the RHS, so LHS = RHS. Hence proved.

Valid where $\cos 3x \neq 0$, $\cos 9x \neq 0$, $\cos 27x \neq 0$, $\cos x \neq 0$.

## PD-MATH-XI-013

30. If S₁, S₂ and S₃ be respectively the sum of n, 2n and 3n terms of a GP prove that

S₁(S₃ - S₂) = (S₂ - S₁)²

**Solution**

Let G be the GP with first term $a$ and common ratio $r$.

**LHS:**

$$S_{n} \left(S_{3 n} - S_{2 n}\right)$$

$$= \frac{a \left(r^{n} - 1\right) \left(- \frac{a \left(r^{2 n} - 1\right)}{r - 1} + \frac{a \left(r^{3 n} - 1\right)}{r - 1}\right)}{r - 1}$$

*Use $S_n = \frac{a(r^n - 1)}{r - 1}$.*

$$= \frac{a^{2} \left(r^{n} - 1\right) \left(r^{3 n} - r^{2 n}\right)}{\left(r - 1\right)^{2}}$$

*Take a common denominator.*

$$= \frac{a^{2} r^{4 n} - 2 a^{2} r^{3 n} + a^{2} r^{2 n}}{\left(r - 1\right)^{2}}$$

*Expand the numerator.*

$$= \frac{a^{2} r^{2 n} \left(r^{n} - 1\right)^{2}}{\left(r - 1\right)^{2}}$$

*Factorise.*

**RHS:**

$$\left(S_{2 n} - S_{n}\right)^{2}$$

$$= \left(- \frac{a \left(r^{n} - 1\right)}{r - 1} + \frac{a \left(r^{2 n} - 1\right)}{r - 1}\right)^{2}$$

*Use $S_n = \frac{a(r^n - 1)}{r - 1}$.*

$$= \frac{a^{2} \left(r^{2 n} - r^{n}\right)^{2}}{\left(r - 1\right)^{2}}$$

*Take a common denominator.*

$$= \frac{a^{2} r^{4 n} - 2 a^{2} r^{3 n} + a^{2} r^{2 n}}{\left(r - 1\right)^{2}}$$

*Expand the numerator.*

$$= \frac{a^{2} r^{2 n} \left(r^{n} - 1\right)^{2}}{\left(r - 1\right)^{2}}$$

*Factorise.*

Both sides reduce to the same expression, so LHS = RHS. Hence proved.

Valid where $r - 1 \neq 0$, $a \neq 0$.

## PD-MATH-XI-015

28. Find the derivative of f(x) from the first principle , where f(x) = x² sin x

**Solution**

Let $f(x) = x^{2} \sin x$.

$$f'(x)$$

$$= \lim_{h \to 0}\left(\frac{- x^{2} \sin x + \left(h + x\right)^{2} \sin\left(h + x\right)}{h}\right)$$

*Use the definition $f'(x) = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}$.*

$$= \lim_{h \to 0}\left(\frac{\left(h + x\right)^{2} \left(- \sin x + \sin\left(h + x\right)\right)}{h} + \frac{\left(- x^{2} + \left(h + x\right)^{2}\right) \sin x}{h}\right)$$

*Write $f(x+h) - f(x) = u(x+h)[v(x+h) - v(x)] + v(x)[u(x+h) - u(x)]$.*

$$= \lim_{h \to 0}\left(\left(h + 2 x\right) \sin x + \frac{2 \left(h + x\right)^{2} \sin \frac{h}{2} \cos\left(\frac{h}{2} + x\right)}{h}\right)$$

*Use the sum-to-product formula, and expand and cancel $h$ in the second term.*

$$= \lim_{h \to 0}\left(\frac{\sin \frac{h}{2}}{\frac{1}{2} h} \left(h + x\right)^{2} \cos\left(\frac{h}{2} + x\right) + \left(h + 2 x\right) \sin x\right)$$

*Arrange the first term to use $\lim_{\theta \to 0} \frac{\sin\theta}{\theta} = 1$.*

$$= x^{2} \cos x + 2 x \sin x$$

*Let $h \to 0$ (using $\lim_{\theta \to 0} \frac{\sin\theta}{\theta} = 1$ where needed).*

Hence $f'(x) = x^{2} \cos x + 2 x \sin x$.

## PD-MATH-XI-020

(a) Using the first principle, find the derivative of $\sqrt{3x + 4}$.

**Solution**

Let $f(x) = \sqrt{3 x + 4}$.

$$f'(x)$$

$$= \lim_{h \to 0}\left(\frac{- \sqrt{3 x + 4} + \sqrt{3 h + 3 x + 4}}{h}\right)$$

*Use the definition $f'(x) = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}$.*

$$= \lim_{h \to 0}\left(\frac{3 h}{h \left(\sqrt{3 x + 4} + \sqrt{3 h + 3 x + 4}\right)}\right)$$

*Multiply the numerator and the denominator by the conjugate.*

$$= \lim_{h \to 0}\left(\frac{3}{\sqrt{3 x + 4} + \sqrt{3 h + 3 x + 4}}\right)$$

*Simplify the numerator and cancel $h$.*

$$= \frac{3}{2 \sqrt{3 x + 4}}$$

*Let $h \to 0$ (using $\lim_{\theta \to 0} \frac{\sin\theta}{\theta} = 1$ where needed).*

Hence $f'(x) = \frac{3}{2 \sqrt{3 x + 4}}$.

## PD-MATH-XI-025

Show that, if $$p, q, r$$ and $$s$$ are real numbers such that, $$pr = 2(q + s)$$, then at least one of the equations $$x^2 + px + q = 0$$, and $$x^2 + rx + s = 0$$ has real roots.

**Solution**

Given: $p r = 2 \left(q + s\right)$.

From the given condition:

$$p r = 2 q + 2 s \implies q = \frac{p r}{2} - s$$

*Make $q$ the subject.*

For $x^{2} + p x + q = 0$ the discriminant is $D_{1} = p^{2} - 4 q$.

For $x^{2} + r x + s = 0$ the discriminant is $D_{2} = r^{2} - 4 s$.

Add them: $D_{1} + D_{2}$

$$p^{2} - 4 q + r^{2} - 4 s$$

$$= p^{2} - 2 p r + r^{2}$$

*Substitute $q = \frac{p r}{2} - s$.*

$$= \left(p - r\right)^{2}$$

*Simplify algebraically.*

A square is never negative, so $D_{1} + D_{2} \geq 0$. The discriminants cannot both be negative, so at least one of them is $\geq 0$: at least one equation has real roots.

## PD-MATH-XI-030

(c) Show that the given statement is true by the method of contradiction:

If x is a real number such that x³ + 8x = 0, thus x = 0

**Solution**

$$x^{3} + 8 x = 0 \iff x \left(x^{2} + 8\right) = 0$$

Suppose, for contradiction, that $x \neq 0$. Then $x^{2} + 8 = 0$.

$$x^{2} + 8 = x^{2} + 8$$

*Complete the square.*

$$x^{2} + 8 > 0$$

*A real square is nonnegative and the constant is positive.*

So $x^{2} + 8$ is never zero for real $x$: a contradiction. Hence $x = 0$.

## PD-MATH-XII-001

(ii) If $e^y(x + 1) = 1$ then show that $\frac{d^2y}{dx^2} = \left(\frac{dy}{dx}\right)^2$ [2]

**Solution**

Given: $e^{y} \left(x + 1\right) = 1$.

From the given condition:

$$\left(x + 1\right) e^{y} = 1 \implies \frac{dy}{dx} \left(x + 1\right) e^{y} + e^{y} = 0$$

*Differentiate both sides with respect to $x$.*

$$\frac{dy}{dx} \left(x + 1\right) e^{y} + e^{y} = 0 \implies \frac{dy}{dx} \left(\frac{dy}{dx} \left(x + 1\right) e^{y} + e^{y}\right) + \frac{dy}{dx} e^{y} + \frac{d^{2}y}{dx^{2}} \left(x + 1\right) e^{y} = 0$$

*Differentiate both sides with respect to $x$.*

$$\frac{dy}{dx} \left(\frac{dy}{dx} \left(x + 1\right) e^{y} + e^{y}\right) + \frac{dy}{dx} e^{y} + \frac{d^{2}y}{dx^{2}} \left(x + 1\right) e^{y} = 0 \implies \frac{d^{2}y}{dx^{2}} = \frac{\frac{dy}{dx} \left(- x \frac{dy}{dx} - \frac{dy}{dx} - 2\right)}{x + 1}$$

*Make $\frac{d^{2}y}{dx^{2}}$ the subject.*

$$\frac{dy}{dx} \left(x + 1\right) e^{y} + e^{y} = 0 \implies \frac{dy}{dx} = - \frac{1}{x + 1}$$

*Make $\frac{dy}{dx}$ the subject.*

**LHS:**

$$\frac{d^{2}y}{dx^{2}}$$

$$= - \frac{\frac{x}{x + 1} - 2 + \frac{1}{x + 1}}{\left(x + 1\right)^{2}}$$

*Substitute $\frac{d^{2}y}{dx^{2}} = \frac{\frac{dy}{dx} \left(- x \frac{dy}{dx} - \frac{dy}{dx} - 2\right)}{x + 1}$ and $\frac{dy}{dx} = - \frac{1}{x + 1}$.*

$$= - \frac{- x - 1}{\left(x + 1\right)^{3}}$$

*Take a common denominator.*

$$= \frac{x + 1}{\left(x + 1\right)^{3}}$$

*Expand the numerator.*

$$= \frac{1}{\left(x + 1\right)^{2}}$$

*Factorise.*

**RHS:**

$$\left(\frac{dy}{dx}\right)^{2}$$

$$= \frac{1}{\left(x + 1\right)^{2}}$$

*Substitute $\frac{dy}{dx} = - \frac{1}{x + 1}$.*

Both sides reduce to the same expression, so LHS = RHS. Hence proved.

## PD-MATH-XII-002

If $y = x^x$ then prove that $\frac{d^2y}{dx^2} - \frac{1}{y}\left(\frac{dy}{dx}\right)^2 - \frac{y}{x} = 0$

**Solution**

Given: $y = x^{x}$.

From the given condition:

$$y = x^{x} \implies \log{\left(y \right)} = x \log{\left(x \right)}$$

*Take logarithms of both sides.*

$$\log{\left(y \right)} = x \log{\left(x \right)} \implies \frac{\frac{dy}{dx}}{y} = \log{\left(x \right)} + 1$$

*Differentiate both sides with respect to $x$.*

$$\frac{\frac{dy}{dx}}{y} = \log{\left(x \right)} + 1 \implies \frac{\frac{d^{2}y}{dx^{2}}}{y} - \frac{\left(\frac{dy}{dx}\right)^{2}}{y^{2}} = \frac{1}{x}$$

*Differentiate both sides with respect to $x$.*

$$\frac{\frac{d^{2}y}{dx^{2}}}{y} - \frac{\left(\frac{dy}{dx}\right)^{2}}{y^{2}} = \frac{1}{x} \implies \frac{d^{2}y}{dx^{2}} = \frac{\left(\frac{dy}{dx}\right)^{2}}{y} + \frac{y}{x}$$

*Make $\frac{d^{2}y}{dx^{2}}$ the subject.*

**LHS:**

$$\frac{d^{2}y}{dx^{2}} - \frac{\left(\frac{dy}{dx}\right)^{2}}{y} - \frac{y}{x}$$

$$= 0$$

*Substitute $\frac{d^{2}y}{dx^{2}} = \frac{\left(\frac{dy}{dx}\right)^{2}}{y} + \frac{y}{x}$.*

This is the RHS, so LHS = RHS. Hence proved.

Valid where $y \neq 0$, $x \neq 0$.

## PD-MATH-XII-003

If $xy = e^{x-y}$, prove that : $\frac{dy}{dx} = \frac{y(x-1)}{x(y+1)}$ [2]

**Solution**

Given: $x y = e^{x - y}$.

From the given condition:

$$x y = e^{x - y} \implies x \frac{dy}{dx} + y = - \frac{dy}{dx} e^{x - y} + e^{x - y}$$

*Differentiate both sides with respect to $x$.*

$$x \frac{dy}{dx} + y = - \frac{dy}{dx} e^{x - y} + e^{x - y} \implies \frac{dy}{dx} = \frac{- y + e^{x - y}}{x + e^{x - y}}$$

*Make $\frac{dy}{dx}$ the subject.*

**LHS:**

$$\frac{dy}{dx}$$

$$= \frac{- y + e^{x - y}}{x + e^{x - y}}$$

*Substitute $\frac{dy}{dx} = \frac{- y + e^{x - y}}{x + e^{x - y}}$.*

**RHS:**

$$\frac{y \left(x - 1\right)}{x \left(y + 1\right)}$$

$$= \frac{x y - y}{x y + x}$$

*Simplify the algebraic fraction.*

$$= \frac{- y + e^{x - y}}{x + e^{x - y}}$$

*Use the given $x y = e^{x - y}$.*

Both sides reduce to the same expression, so LHS = RHS. Hence proved.

Valid where $x \neq 0$, $y + 1 \neq 0$, $y \neq 0$.

## PD-MATH-XII-004

If $logy = \tan^{-1} x$, prove that $(1 + x^2)y_2 + (2x - 1)y_1 = 0$ [4]

**Solution**

Given: $log\left(y\right) = \tan^{-1}\left(x\right)$.

From the given condition:

$$\log{\left(y \right)} = \tan^{-1} x \implies \frac{y_{1}}{y} = \frac{1}{x^{2} + 1}$$

*Differentiate both sides with respect to $x$.*

$$\frac{y_{1}}{y} = \frac{1}{x^{2} + 1} \implies \frac{y_{2}}{y} - \frac{y_{1}^{2}}{y^{2}} = - \frac{2 x}{\left(x^{2} + 1\right)^{2}}$$

*Differentiate both sides with respect to $x$.*

$$\frac{y_{1}}{y} = \frac{1}{x^{2} + 1} \implies y_{1} = \frac{y}{x^{2} + 1}$$

*Make $y_{1}$ the subject.*

$$\frac{y_{2}}{y} - \frac{y_{1}^{2}}{y^{2}} = - \frac{2 x}{\left(x^{2} + 1\right)^{2}} \implies y_{2} = \frac{x^{4} y_{1}^{2} + 2 x^{2} y_{1}^{2} - 2 x y^{2} + y_{1}^{2}}{y \left(x^{4} + 2 x^{2} + 1\right)}$$

*Make $y_{2}$ the subject.*

**LHS:**

$$\left(1 + x^{2}\right) y_{2} + \left(2 x - 1\right) y_{1}$$

$$= \frac{y \left(2 x - 1\right)}{x^{2} + 1} + \frac{\left(x^{2} + 1\right) \left(x^{4} y_{1}^{2} + 2 x^{2} y_{1}^{2} - 2 x y^{2} + y_{1}^{2}\right)}{y \left(x^{4} + 2 x^{2} + 1\right)}$$

*Substitute $y_{1} = \frac{y}{x^{2} + 1}$ and $y_{2} = \frac{x^{4} y_{1}^{2} + 2 x^{2} y_{1}^{2} - 2 x y^{2} + y_{1}^{2}}{y \left(x^{4} + 2 x^{2} + 1\right)}$.*

$$= \frac{\left(x^{2} y_{1} - y + y_{1}\right) \left(x^{2} y_{1} + y + y_{1}\right)}{y \left(x^{2} + 1\right)}$$

*Combine and factor the algebraic expression.*

$$= \frac{\left(\frac{x^{2} y}{x^{2} + 1} - y + \frac{y}{x^{2} + 1}\right) \left(\frac{x^{2} y}{x^{2} + 1} + y + \frac{y}{x^{2} + 1}\right)}{y \left(x^{2} + 1\right)}$$

*Substitute $y_{1} = \frac{y}{x^{2} + 1}$.*

$$= 0$$

*Cancel.*

This is the RHS, so LHS = RHS. Hence proved.

## PD-MATH-XII-010

(i) Prove that $2 \tan^{-1} \left(\frac{1}{5}\right) + \cos^{-1} \left(\frac{7}{5\sqrt{2}}\right) + 2 \tan^{-1} \left(\frac{1}{8}\right) = \frac{\pi}{4}$

**Solution**

**LHS:**

$$2 \tan^{-1}\left(\frac{1}{5}\right) + \cos^{-1}\left(\frac{7}{5 \sqrt{2}}\right) + 2 \tan^{-1}\left(\frac{1}{8}\right)$$

$$= \tan^{-1}\left(\frac{1}{7}\right) + 2 \tan^{-1}\left(\frac{1}{8}\right) + 2 \tan^{-1}\left(\frac{1}{5}\right)$$

*Use $\cos^{-1} x = \tan^{-1}\frac{\sqrt{1 - x^{2}}}{x}$, valid as $0 < x \le 1$.*

$$= \tan^{-1}\left(\frac{1}{7}\right) + \tan^{-1}\left(\frac{16}{63}\right) + 2 \tan^{-1}\left(\frac{1}{5}\right)$$

*Use $2\tan^{-1} x = \tan^{-1}\frac{2x}{1 - x^{2}}$, valid as $|x| < 1$.*

$$= \tan^{-1}\left(\frac{7}{17}\right) + 2 \tan^{-1}\left(\frac{1}{5}\right)$$

*Use $\tan^{-1} x + \tan^{-1} y = \tan^{-1}\frac{x + y}{1 - xy}$, valid as $xy < 1$.*

$$= \tan^{-1}\left(\frac{7}{17}\right) + \tan^{-1}\left(\frac{5}{12}\right)$$

*Use $2\tan^{-1} x = \tan^{-1}\frac{2x}{1 - x^{2}}$, valid as $|x| < 1$.*

$$= \frac{\pi}{4}$$

*Use $\tan^{-1} x + \tan^{-1} y = \tan^{-1}\frac{x + y}{1 - xy}$, valid as $xy < 1$.*

This is the RHS, so LHS = RHS. Hence proved.

## PD-MATH-XII-011

# Question 14

[3+3=6]

a) Prove that $$\cot^{-1}\left[\frac{\sqrt{1+sinx}+\sqrt{1-sinx}}{\sqrt{1+sinx}-\sqrt{1-sinx}}\right]=\frac{x}{2}, x\in(0,\frac{\pi}{4})$$

**Solution**

**LHS:**

$$\cot^{-1}\left(\frac{\sqrt{1 + \sin x} + \sqrt{1 - \sin x}}{\sqrt{1 + \sin x} - \sqrt{1 - \sin x}}\right)$$

$$= \cot^{-1}\left(\frac{\cos\left(\frac{x}{2}\right)}{\sin \frac{x}{2}}\right)$$

*Use $1 \pm \sin x = \left(\cos\frac{x}{2} \pm \sin\frac{x}{2}\right)^{2}$ (and $1 + \cos x = 2\cos^{2}\frac{x}{2}$, $1 - \cos x = 2\sin^{2}\frac{x}{2}$); the root is the nonnegative one on the given interval.*

$$= \frac{x}{2}$$

*Use $\cot^{-1}(\cot u) = u$ for $0 < u < \pi$ (and $\tan^{-1}(\tan u) = u$ for $-\frac{\pi}{2} < u < \frac{\pi}{2}$); the given interval puts $u$ there.*

This is the RHS, so LHS = RHS. Hence proved.

Valid where $\sin x + 1 \geq 0$, $1 - \sin x \geq 0$, $- \sqrt{1 - \sin x} + \sqrt{\sin x + 1} \neq 0$, $x > 0$, $- x + \frac{\pi}{4} > 0$.

## PD-MATH-XII-016

(i) Show that the height of a cylinder of maximum volume that can be inscribed in a sphere of radius R is $$\frac{2R}{\sqrt{3}}$$. Find the volume of the largest cylinder inscribed in a sphere of radius R.

**Solution**

Given: $r^{2} + \left(\frac{h}{2}\right)^{2} = R^{2}$.

From the given condition:

$$\frac{h^{2}}{4} + r^{2} = R^{2} \implies r^{2} = R^{2} - \frac{h^{2}}{4}$$

*Make $r^{2}$ the subject.*

Write the quantity in terms of one variable:

$$\pi r^{2} h$$

$$= \pi h \left(R^{2} - \frac{h^{2}}{4}\right)$$

*Substitute $r^{2} = R^{2} - \frac{h^{2}}{4}$.*

Differentiate:

$$\frac{d}{d h} \pi h \left(R^{2} - \frac{h^{2}}{4}\right)$$

$$= - \frac{\pi h^{2}}{2} + \pi \left(R^{2} - \frac{h^{2}}{4}\right)$$

*Differentiate.*

$$= \pi R^{2} - \frac{3 \pi h^{2}}{4}$$

*Simplify algebraically.*

$$\pi R^{2} - \frac{3 \pi h^{2}}{4} = 0 \implies h = \frac{2 \sqrt{3} R}{3}$$

*Set the derivative to zero and keep the value in the domain.*

$$\frac{d^{2}}{d h^{2}} \pi h \left(R^{2} - \frac{h^{2}}{4}\right) = - \sqrt{3} \pi R \text{ at } h = \frac{2 \sqrt{3} R}{3}$$

*The second derivative is negative there, so this is a maximum; it is the only critical point, so the maximum is overall.*

At the optimum, $h = \frac{2 \sqrt{3} R}{3}$: both sides equal $\frac{2 \sqrt{3} R}{3}$.

At the optimum, $\pi h r^{2} = \frac{4 \sqrt{3} \pi R^{3}}{9}$: both sides equal $\frac{4 \sqrt{3} \pi R^{3}}{9}$.

The maximum value is $\frac{4 \sqrt{3} \pi R^{3}}{9}$.

## PD-MATH-XII-017

Prove that the area of a right-angled triangle of given hypotenuse is maximum when the triangle is isosceles.

[6]

**Solution**

Given: $a^{2} + b^{2} = c^{2}$.

From the given condition:

$$a^{2} + b^{2} = c^{2} \implies b^{2} = - a^{2} + c^{2}$$

*Make $b^{2}$ the subject.*

$$b^{2} = - a^{2} + c^{2} \implies b = \sqrt{- a^{2} + c^{2}}$$

*Take the positive root, since $b > 0$.*

Write the quantity in terms of one variable:

$$\frac{a b}{2}$$

$$= \frac{a \sqrt{- a^{2} + c^{2}}}{2}$$

*Substitute $b = \sqrt{- a^{2} + c^{2}}$.*

Differentiate:

$$\frac{d}{d a} \frac{a \sqrt{- a^{2} + c^{2}}}{2}$$

$$= - \frac{a^{2}}{2 \sqrt{- a^{2} + c^{2}}} + \frac{\sqrt{- a^{2} + c^{2}}}{2}$$

*Differentiate.*

$$= \frac{a^{2} \sqrt{- a^{2} + c^{2}}}{2 a^{2} - 2 c^{2}} + \frac{\sqrt{- a^{2} + c^{2}}}{2}$$

*Rationalise each denominator.*

$$= \frac{\sqrt{- a^{2} + c^{2}} \left(2 a^{2} - c^{2}\right)}{2 a^{2} - 2 c^{2}}$$

*Simplify algebraically.*

$$= \frac{- a^{2} + \frac{c^{2}}{2}}{\sqrt{- a^{2} + c^{2}}}$$

*Rationalise each denominator.*

$$\frac{- a^{2} + \frac{c^{2}}{2}}{\sqrt{- a^{2} + c^{2}}} = 0 \implies a = \frac{\sqrt{2} c}{2}$$

*Set the derivative to zero and keep the value in the domain.*

$$\frac{d^{2}}{d a^{2}} \frac{a \sqrt{- a^{2} + c^{2}}}{2} = -2 \text{ at } a = \frac{\sqrt{2} c}{2}$$

*The second derivative is negative there, so this is a maximum; it is the only critical point, so the maximum is overall.*

At the optimum, $a = b$: both sides equal $\frac{\sqrt{2} c}{2}$.

The maximum value is $\frac{c^{2}}{4}$.

## PD-MATH-XII-018

i) A given quantity of metal is to be cast into a half cylinder with a rectangular base and semi-circular ends. Show that the total surface area is minimum when the ratio of the length of the cylinder to the diameter of its semi-circular ends is $\pi: (\pi + 2)$.

**Solution**

Given: $V = \frac{\pi r^{2} L}{2}$.

From the given condition:

$$V = \frac{\pi L r^{2}}{2} \implies L = \frac{2 V}{\pi r^{2}}$$

*Make $L$ the subject.*

Write the quantity in terms of one variable:

$$\pi r^{2} + \pi r L + 2 r L$$

$$= \frac{4 V}{\pi r} + \frac{2 V}{r} + \pi r^{2}$$

*Substitute $L = \frac{2 V}{\pi r^{2}}$.*

Differentiate:

$$\frac{d}{d r} \left(\frac{4 V}{\pi r} + \frac{2 V}{r} + \pi r^{2}\right)$$

$$= - \frac{2 V}{r^{2}} - \frac{4 V}{\pi r^{2}} + 2 \pi r$$

*Differentiate.*

$$- \frac{2 V}{r^{2}} - \frac{4 V}{\pi r^{2}} + 2 \pi r = 0 \implies r = \frac{\sqrt[3]{2 V + \pi V}}{\pi^{\frac{2}{3}}}$$

*Set the derivative to zero and keep the value in the domain.*

$$\frac{d^{2}}{d r^{2}} \left(\frac{4 V}{\pi r} + \frac{2 V}{r} + \pi r^{2}\right) = 6 \pi \text{ at } r = \frac{\sqrt[3]{2 V + \pi V}}{\pi^{\frac{2}{3}}}$$

*The second derivative is positive there, so this is a minimum; it is the only critical point, so the minimum is overall.*

At the optimum, $\frac{L}{2 r} = \frac{\pi}{2 + \pi}$: both sides equal $\frac{\pi}{2 + \pi}$.

The minimum value is $\frac{3 V^{\frac{2}{3}} \left(2 + \pi\right)^{\frac{2}{3}}}{\sqrt[3]{\pi}}$.

## PD-MATH-XII-019

Show that the function f(x) = x³ − 3x² + 6x − 100 is increasing on R.

[2]

**Solution**

Let $f(x) = x^{3} - 3 x^{2} + 6 x - 100$.

$$\frac{d}{dx}\left(f(x)\right)$$

$$= 3 x^{2} - 6 x + 6$$

*Differentiate.*

$$= 3 \left(x - 1\right)^{2} + 3$$

*Complete the square.*

$$3 \left(x - 1\right)^{2} + 3 > 0$$

*A real square is nonnegative and the constant is positive.*

Since the derivative is positive, $f$ is increasing.

## PD-MATH-XII-021

Given that the total cost function for x units of a commodity is $$C(x) = \frac{x^3}{3} + 3x^2 - 7x + 16$$. Find

(a) the marginal cost (MC)
(b) the average cost (AC)
(c) Prove that marginal average cost (MAC) \(\frac{x(MC) - C(x)}{x^2}\) [4]

**Solution**

**Part 1: MC**

$$MC = \frac{d}{dx}\left(C\left(x\right)\right)$$

$$= \frac{d}{d x} \left(\frac{x^{3}}{3} + 3 x^{2} - 7 x + 16\right)$$

*Use the definition.*

$$= x^{2} + 6 x - 7$$

*Differentiate.*


**Part 2: AC**

$$AC = \frac{C\left(x\right)}{x}$$

$$= \frac{\frac{x^{3}}{3} + 3 x^{2} - 7 x + 16}{x}$$

*Use the definition.*

$$= \frac{x^{3} + 9 x^{2} - 21 x + 48}{3 x}$$

*Multiply the numerator and the denominator by 3.*

$$= \frac{x^{2}}{3} + 3 x - 7 + \frac{16}{x}$$

*Simplify.*


Valid where $x \neq 0$.

**Part 3: $\frac{d}{dx}\left(\frac{C\left(x\right)}{x}\right) = \frac{x \frac{d}{dx}\left(C\left(x\right)\right) - C\left(x\right)}{x^{2}}$**

**LHS:**

$$\frac{d}{dx}\left(\frac{C\left(x\right)}{x}\right)$$

$$= \frac{\frac{d}{d x} C\left(x\right)}{x} - \frac{C\left(x\right)}{x^{2}}$$

*Differentiate.*

$$= \frac{x \frac{d}{d x} C\left(x\right) - C\left(x\right)}{x^{2}}$$

*Simplify algebraically.*

This is the RHS, so LHS = RHS. Hence proved.

Valid where $x \neq 0$.

## PD-MATH-XII-022

20. (a) The total cost function for $x$ units is given by $C(x) = \sqrt{6x + 5} + 2500$. Show that the marginal cost decreases as the output $x$ increases. [2]

**Solution**

Let $f(x) = \frac{d}{dx}\left(C\left(x\right)\right)$.

$$\frac{d}{dx}\left(f(x)\right)$$

$$= \frac{d^{2}}{d x^{2}} \left(\sqrt{6 x + 5} + 2500\right)$$

*Use the definition.*

$$= - \frac{9}{\left(6 x + 5\right)^{\frac{3}{2}}}$$

*Differentiate.*

$$- \frac{9}{\left(6 x + 5\right)^{\frac{3}{2}}} < 0$$

*Each factor has a fixed sign for the allowed values of $x$.*

Since the derivative is negative, $f$ is decreasing.

## PD-MATH-XII-032

Prove that $\int_0^a f(x)\,dx = \int_0^a f(a-x)\,dx$, hence evaluate $\int_0^\pi \frac{x\sin x}{1+\cos^2 x}\,dx$.

**Solution**

**Part 1: $\int_{0}^{a} f\left(x\right)\,dx = \int_{0}^{a} f\left(a - x\right)\,dx$**

**LHS:**

$$\int_{0}^{a} f\left(x\right)\,dx$$

$$= \int\limits_{0}^{a} f{\left(a - t \right)}\, dt$$

*Put $x = a - t$, so $dx = -dt$, and change the limits.*

$$= \int\limits_{0}^{a} f{\left(a - x \right)}\, dx$$

*A definite integral does not depend on the letter used for its variable.*

This is the RHS, so LHS = RHS. Hence proved.

**Part 2: $\int_{0}^{\pi} \frac{x \sin x}{1 + \cos^{2} x}\,dx = \frac{\pi^{2}}{4}$**

From the earlier part: $\int\limits_{0}^{a} f{\left(x \right)}\, dx = \int\limits_{0}^{a} f{\left(a - x \right)}\, dx$.

**LHS:**

$$\int_{0}^{\pi} \frac{x \sin x}{1 + \cos^{2} x}\,dx$$

$$= \frac{\int\limits_{0}^{\pi} \frac{x \sin x}{\cos^{2} x + 1}\, dx + \int\limits_{0}^{\pi} \frac{\left(\pi - x\right) \sin x}{\cos^{2} x + 1}\, dx}{2}$$

*Use $\int_a^b f(x)\,dx = \int_a^b f(a+b-x)\,dx$, so $I$ is half the sum of the two.*

$$= \frac{\int\limits_{0}^{\pi} \left(\frac{x \sin x}{\cos^{2} x + 1} + \frac{\left(\pi - x\right) \sin x}{\cos^{2} x + 1}\right)\, dx}{2}$$

*Add the integrals over the same limits.*

$$= \frac{\int\limits_{0}^{\pi} \frac{\pi \sin x}{\cos^{2} x + 1}\, dx}{2}$$

*Simplify the integrand.*

$$= \frac{\pi \int\limits_{0}^{\pi} \frac{\sin x}{\cos^{2} x + 1}\, dx}{2}$$

*Take the constant outside the integral.*

$$= \frac{\pi \left[- \tan^{-1}\left(\cos\left(x\right)\right)\right]_{0}^{\pi}}{2}$$

*Integrate.*

$$= \frac{\pi \left(\frac{\pi}{4} + \frac{\pi}{4}\right)}{2}$$

*Substitute the limits.*

$$= \frac{\pi^{2}}{4}$$

*Simplify.*

This is the RHS, so LHS = RHS. Hence proved.

## PD-MATH-XII-033

(i) Prove: $$\int_{\frac{\pi}{4}}^{\frac{3\pi}{4}} \frac{x dx}{1 + \sin x} = (\sqrt{2} - 1)\pi$$

**Solution**

**LHS:**

$$\int_{\frac{\pi}{4}}^{\frac{3 \pi}{4}} \frac{x}{1 + \sin x}\,dx$$

$$= \frac{\int\limits_{\frac{\pi}{4}}^{\frac{3 \pi}{4}} \frac{x}{\sin x + 1}\, dx + \int\limits_{\frac{\pi}{4}}^{\frac{3 \pi}{4}} \frac{\pi - x}{\sin x + 1}\, dx}{2}$$

*Use $\int_a^b f(x)\,dx = \int_a^b f(a+b-x)\,dx$, so $I$ is half the sum of the two.*

$$= \frac{\int\limits_{\frac{\pi}{4}}^{\frac{3 \pi}{4}} \left(\frac{x}{\sin x + 1} + \frac{\pi - x}{\sin x + 1}\right)\, dx}{2}$$

*Add the integrals over the same limits.*

$$= \frac{\int\limits_{\frac{\pi}{4}}^{\frac{3 \pi}{4}} \frac{\pi}{\sin x + 1}\, dx}{2}$$

*Simplify the integrand.*

$$= \frac{\pi \int\limits_{\frac{\pi}{4}}^{\frac{3 \pi}{4}} \frac{1}{\sin x + 1}\, dx}{2}$$

*Take the constant outside the integral.*

$$= \frac{\pi \int\limits_{\frac{\pi}{4}}^{\frac{3 \pi}{4}} \frac{1}{2 \sin^{2}\left(\frac{x}{2} + \frac{\pi}{4}\right)}\, dx}{2}$$

*Use $1 + \sin x = 2\cos^2\left(\frac{\pi}{4} - \frac{x}{2}\right)$ (and the like for $1 - \sin x$, $1 \pm \cos x$).*

$$= \frac{\pi \left[- \cot\left(\frac{x}{2} + \frac{\pi}{4}\right)\right]_{\frac{\pi}{4}}^{\frac{3 \pi}{4}}}{2}$$

*Integrate.*

$$= \frac{\pi \left(\left(-1 + \sqrt{2}\right) - \left(1 - \sqrt{2}\right)\right)}{2}$$

*Substitute the limits.*

$$= \pi \left(-1 + \sqrt{2}\right)$$

*Simplify.*

This is the RHS, so LHS = RHS. Hence proved.

## PD-MATH-XII-034

# Question: 18

[4]

Prove that the curves $y^2 = 4x$ and $x^2 = 4y$ divide the area of the bounded by $x=0, x=4, y=0$ and $y=4$ into three equal parts.

**Solution**

**Part 1: $\int_{0}^{4} \frac{x^{2}}{4}\,dx = \frac{16}{3}$**

**LHS:**

$$\int_{0}^{4} \frac{x^{2}}{4}\,dx$$

$$= \left[\frac{x^{3}}{12}\right]_{0}^{4}$$

*Integrate.*

$$= \frac{16}{3}$$

*Substitute the limits.*

This is the RHS, so LHS = RHS. Hence proved.

**Part 2: $\int_{0}^{4} \left(2 \sqrt{x} - \frac{x^{2}}{4}\right)\,dx = \frac{16}{3}$**

From the earlier part: $\int\limits_{0}^{4} \frac{x^{2}}{4}\, dx = \frac{16}{3}$.

**LHS:**

$$\int_{0}^{4} \left(2 \sqrt{x} - \frac{x^{2}}{4}\right)\,dx$$

$$= \left[\frac{4 x^{\frac{3}{2}}}{3} - \frac{x^{3}}{12}\right]_{0}^{4}$$

*Integrate.*

$$= \frac{16}{3}$$

*Substitute the limits.*

This is the RHS, so LHS = RHS. Hence proved.

**Part 3: $\int_{0}^{4} \left(4 - 2 \sqrt{x}\right)\,dx = \frac{16}{3}$**

From the earlier part: $\int\limits_{0}^{4} \frac{x^{2}}{4}\, dx = \frac{16}{3}$.

From the earlier part: $\int\limits_{0}^{4} \left(2 \sqrt{x} - \frac{x^{2}}{4}\right)\, dx = \frac{16}{3}$.

**LHS:**

$$\int_{0}^{4} \left(4 - 2 \sqrt{x}\right)\,dx$$

$$= \left[- \frac{4 x^{\frac{3}{2}}}{3} + 4 x\right]_{0}^{4}$$

*Integrate.*

$$= \frac{16}{3}$$

*Substitute the limits.*

This is the RHS, so LHS = RHS. Hence proved.

## PD-MATH-XII-035

Show that the general solution of the differential equation $x \frac{d^2y}{dx^2} + 2 \frac{dy}{dx} - xy + x^2 - 2 = 0$, is given by, $xy = ae^x + be^{-x} + x^2$, where $a$ and $b$ are arbitrary constants.

[2]

**Solution**

Given: $x y = a e^{x} + b e^{-x} + x^{2}$.

From the given condition:

$$x y = a e^{x} + b e^{- x} + x^{2} \implies x \frac{dy}{dx} + y = a e^{x} - b e^{- x} + 2 x$$

*Differentiate both sides with respect to $x$.*

$$x \frac{dy}{dx} + y = a e^{x} - b e^{- x} + 2 x \implies x \frac{d^{2}y}{dx^{2}} + 2 \frac{dy}{dx} = a e^{x} + b e^{- x} + 2$$

*Differentiate both sides with respect to $x$.*

$$x \frac{d^{2}y}{dx^{2}} + 2 \frac{dy}{dx} = a e^{x} + b e^{- x} + 2 \implies \frac{dy}{dx} = \frac{a e^{x}}{2} + \frac{b e^{- x}}{2} - \frac{x \frac{d^{2}y}{dx^{2}}}{2} + 1$$

*Make $\frac{dy}{dx}$ the subject.*

$$x y = a e^{x} + b e^{- x} + x^{2} \implies y = \frac{a e^{x} + b e^{- x} + x^{2}}{x}$$

*Make $y$ the subject.*

**LHS:**

$$x \frac{d^{2}y}{dx^{2}} + 2 \frac{dy}{dx} - x y + x^{2} - 2$$

$$= 0$$

*Substitute $\frac{dy}{dx} = \frac{a e^{x}}{2} + \frac{b e^{- x}}{2} - \frac{x \frac{d^{2}y}{dx^{2}}}{2} + 1$ and $y = \frac{a e^{x} + b e^{- x} + x^{2}}{x}$.*

This is the RHS, so LHS = RHS. Hence proved.

Valid where $x \neq 0$.

# Readability review

For a mathematics teacher. Each answer below was produced and checked by code (`mathcore`); the maths has passed the checker, so this review is about presentation only.

For each answer, score each line 1–5 (5 = exactly as you would want it in class) and add a comment where something should change. About 3 minutes per answer.

Sample: 12 answers, at least one per solving method, seed 20261117.

---

## PD-MATH-VII-002

20.

In the given diagram, $\triangle PQR$ is an isosceles triangle. S and T are the midpoints of PQ and PR respectively. Prove that $RS = QT$.

**Solution**

Since $S$ and $T$ are midpoints, $PS=\tfrac12 PQ$ and $PT=\tfrac12 PR$. The isosceles condition $PQ=PR$ therefore gives $PS=PT$.

Also, $\angle RPS=\angle QPT$: both are the angle at $P$ between $PQ$ and $PR$.

Thus $\triangle PRS\cong\triangle PQT$ by SAS, with $PR=PQ$, $PS=PT$, and equal included angles. Corresponding sides give $RS=QT$.

*Method: `geometry`. Steps shown: 4.*

| Check | Score (1–5) | Comment |
|---|---|---|
| Uses a method taught for this class |  |  |
| Each step can be followed by a student |  |  |
| Notation matches the classroom (sin A, cosec, degrees) |  |  |
| Conditions (where it is valid) are stated sensibly |  |  |
| Would receive full marks as written |  |  |

---

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

*Method: `identity`. Steps shown: 3.*

| Check | Score (1–5) | Comment |
|---|---|---|
| Uses a method taught for this class |  |  |
| Each step can be followed by a student |  |  |
| Notation matches the classroom (sin A, cosec, degrees) |  |  |
| Conditions (where it is valid) are stated sensibly |  |  |
| Would receive full marks as written |  |  |

---

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

*Method: `polynomial`. Steps shown: 3.*

| Check | Score (1–5) | Comment |
|---|---|---|
| Uses a method taught for this class |  |  |
| Each step can be followed by a student |  |  |
| Notation matches the classroom (sin A, cosec, degrees) |  |  |
| Conditions (where it is valid) are stated sensibly |  |  |
| Would receive full marks as written |  |  |

---

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

*Method: `find_value`. Steps shown: 4.*

| Check | Score (1–5) | Comment |
|---|---|---|
| Uses a method taught for this class |  |  |
| Each step can be followed by a student |  |  |
| Notation matches the classroom (sin A, cosec, degrees) |  |  |
| Conditions (where it is valid) are stated sensibly |  |  |
| Would receive full marks as written |  |  |

---

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

*Method: `difference`. Steps shown: 3.*

| Check | Score (1–5) | Comment |
|---|---|---|
| Uses a method taught for this class |  |  |
| Each step can be followed by a student |  |  |
| Notation matches the classroom (sin A, cosec, degrees) |  |  |
| Conditions (where it is valid) are stated sensibly |  |  |
| Would receive full marks as written |  |  |

---

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

*Method: `conditional`. Steps shown: 5.*

| Check | Score (1–5) | Comment |
|---|---|---|
| Uses a method taught for this class |  |  |
| Each step can be followed by a student |  |  |
| Notation matches the classroom (sin A, cosec, degrees) |  |  |
| Conditions (where it is valid) are stated sensibly |  |  |
| Would receive full marks as written |  |  |

---

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

*Method: `first_principles`. Steps shown: 4.*

| Check | Score (1–5) | Comment |
|---|---|---|
| Uses a method taught for this class |  |  |
| Each step can be followed by a student |  |  |
| Notation matches the classroom (sin A, cosec, degrees) |  |  |
| Conditions (where it is valid) are stated sensibly |  |  |
| Would receive full marks as written |  |  |

---

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

*Method: `derivative_relation`. Steps shown: 10.*

| Check | Score (1–5) | Comment |
|---|---|---|
| Uses a method taught for this class |  |  |
| Each step can be followed by a student |  |  |
| Notation matches the classroom (sin A, cosec, degrees) |  |  |
| Conditions (where it is valid) are stated sensibly |  |  |
| Would receive full marks as written |  |  |

---

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

*Method: `extremum`. Steps shown: 8.*

| Check | Score (1–5) | Comment |
|---|---|---|
| Uses a method taught for this class |  |  |
| Each step can be followed by a student |  |  |
| Notation matches the classroom (sin A, cosec, degrees) |  |  |
| Conditions (where it is valid) are stated sensibly |  |  |
| Would receive full marks as written |  |  |

---

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

*Method: `evaluate+identity`. Steps shown: 7.*

| Check | Score (1–5) | Comment |
|---|---|---|
| Uses a method taught for this class |  |  |
| Each step can be followed by a student |  |  |
| Notation matches the classroom (sin A, cosec, degrees) |  |  |
| Conditions (where it is valid) are stated sensibly |  |  |
| Would receive full marks as written |  |  |

---

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

*Method: `monotonic`. Steps shown: 3.*

| Check | Score (1–5) | Comment |
|---|---|---|
| Uses a method taught for this class |  |  |
| Each step can be followed by a student |  |  |
| Notation matches the classroom (sin A, cosec, degrees) |  |  |
| Conditions (where it is valid) are stated sensibly |  |  |
| Would receive full marks as written |  |  |

---

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

*Method: `definite_integral`. Steps shown: 9.*

| Check | Score (1–5) | Comment |
|---|---|---|
| Uses a method taught for this class |  |  |
| Each step can be followed by a student |  |  |
| Notation matches the classroom (sin A, cosec, degrees) |  |  |
| Conditions (where it is valid) are stated sensibly |  |  |
| Would receive full marks as written |  |  |


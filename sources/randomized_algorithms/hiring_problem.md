# The Hiring Problem: Going Beyond Secretaries

## Sources

This summary is based on the slide deck **“The Hiring Problem: Going Beyond Secretaries”**, available at:
[https://theory.stanford.edu/~sergei/slides/hiring-dagstuhl.pdf](https://theory.stanford.edu/~sergei/slides/hiring-dagstuhl.pdf)

**Authors:** Sergei Vassilvitskii, Andrei Broder, Adam Kirsch, Ravi Kumar, Michael Mitzenmacher, and Eli Upfal. The title slide lists affiliations as Yahoo!, Harvard, and Brown. 

---

## 1. The Classical Secretary Problem

The classical **secretary problem** studies sequential decision-making under uncertainty.

### Problem setup

* There are `n` candidates.
* Candidates are interviewed one at a time.
* After each interview, the decision-maker must either:

  * accept the candidate, or
  * reject the candidate permanently.
* The goal is to maximize the probability of selecting the single best candidate.

The slides emphasize that the problem is not really about secretaries, but about **optimal stopping** and **decision-making under uncertainty**. 

---

## 2. From Secretary Selection to Hiring

The deck generalizes the classical secretary problem to a more realistic hiring situation.

Instead of hiring exactly one person, imagine a growing startup that needs to hire many employees. The company wants good employees, but it cannot wait indefinitely for the perfect candidate. 

### Central trade-off

The hiring problem studies the trade-off between:

* the **number of interviews** required,
* the **number of people hired**, and
* the **average quality** of the hired employees.

This turns the problem from “choose the best single candidate” into a repeated online hiring process.

---

## 3. Hiring Model

The model used in the slides is deliberately simple.

### Assumptions

* Candidates arrive one at a time.
* Each candidate has an independent quality score.
* Candidate quality is modeled as:

[
q_i \sim \mathrm{Unif}(0,1)
]

* During each interview:

  * the candidate’s quality score is observed,
  * the decision-maker chooses whether to hire or reject.

The slides note that other distributions can be handled, but the talk focuses on the uniform case. 

---

## 4. Basic Hiring Strategies

The slides compare several simple online hiring strategies.

### 4.1 Threshold hiring

Set a fixed threshold `t`.

Hire candidate `i` if:

[
q_i \geq t
]

This is simple, but it has an obvious limitation: the expected quality does not improve over time.

For threshold `t`:

[
\text{Hiring rate} = 1 - t
]

[
\text{Average quality} \to \frac{1+t}{2}
]

So the organization reaches a fixed quality level, but quality **stagnates**. 

---

### 4.2 Maximum hiring

Hire a candidate only if the candidate is better than everyone already hired.

This produces very high-quality employees, because each new hire improves the current maximum. However, the process becomes extremely slow: as quality approaches 1, finding an even better candidate becomes increasingly unlikely. 

The analysis uses the **gap** between perfect quality and current employee quality:

[
g_i = 1 - q_{h_i}
]

where (h_i) is the (i)-th hired candidate.

Conditioned on the previous gap:

[
g_n \sim \mathrm{Unif}(0, g_{n-1})
]

Therefore:

[
E[g_n \mid g_{n-1}] = \frac{g_{n-1}}{2}
]

and:

[
E[g_n] = \frac{1-q}{2^n}
]

The qualitative conclusion is:

* quality improves very quickly,
* but hiring becomes extremely slow.

---

## 5. Lake Wobegon Strategies

The slides introduce **Lake Wobegon strategies**, named after the joke that everyone is “above average.”

The idea is to hire candidates who are above the current average level of the organization. The slides consider two variants:

1. **Hire above the mean**
2. **Hire above the median**

This is more adaptive than fixed threshold hiring, because the hiring standard rises as the organization improves. 

---

## 6. Hiring Above the Mean

In the **above-mean** strategy:

* start with an employee of quality `q`,
* after each hire, compute the current mean quality,
* hire the next candidate whose score is above that mean.

The slides analyze the gap:

[
g_i = 1 - q_{h_i}
]

The key result is that after `n` hires, the average quality approaches:

[
1 - \Theta\left(\frac{1}{\sqrt{n}}\right)
]

The time required to hire `n` employees is approximately:

[
\Theta(n^{3/2})
]

The slides also note that the concentration behavior is weak, and that hiring above the mean converges to a log-normal distribution. 

### Interpretation

Hiring above the mean gives a reasonable compromise:

* quality improves over time,
* hiring is much faster than maximum hiring,
* but quality improves only at a (1/\sqrt{n}) rate.

---

## 7. Hiring Above the Median

In the **above-median** strategy:

* maintain an odd number of employees, written as (2k+1),
* compute the median employee quality (m_k),
* hire candidates whose quality is above the current median.

The slides show an inductive argument: if the current employees above the median are distributed uniformly on ((m_k, 1)), then after hiring new above-median candidates, the same structure is preserved for the next step. 

### Main results

The median quality after `n` hires improves roughly as:

[
1 - \frac{1}{n}
]

However, the mean gap behaves worse:

[
\Theta\left(\frac{\log n}{n}\right)
]

The time required to hire `n` employees is:

[
\Theta(n^2)
]

The slides again note weak concentration behavior. 

### Interpretation

Hiring above the median produces stronger quality improvement than hiring above the mean, but it requires more interviews.

---

## 8. Comparison of Strategies

| Strategy        | Rule                                        |            Quality behavior |                         Hiring speed | Main weakness      |
| --------------- | ------------------------------------------- | --------------------------: | -----------------------------------: | ------------------ |
| Fixed threshold | Hire if (q_i \geq t)                        |        Approaches ((1+t)/2) |                 Constant-rate hiring | Quality stagnates  |
| Maximum hiring  | Hire only if better than all previous hires |           Very high quality |                       Extremely slow | Too few hires      |
| Above mean      | Hire if above current mean                  |    (1 - \Theta(1/\sqrt{n})) | (\Theta(n^{3/2})) time for `n` hires | Weak concentration |
| Above median    | Hire if above current median                | Mean gap (\Theta(\log n/n)) |     (\Theta(n^2)) time for `n` hires | Slower hiring      |

---

## 9. Extensions Mentioned in the Slides

The final slides mention several possible extensions:

* **Interview preprocessing**
* **Self-selection**, where applicant quality may increase over time
* **Noisy estimates** of candidate scores
* **Firing policies**, such as periodically firing the bottom 10%
* Similar analysis for median-based firing and replacement strategies
* Additional extensions beyond the scope of the talk 

---

## 10. Core Takeaway

The deck’s central point is that the classical secretary problem is too narrow for realistic hiring. Real organizations often need to hire multiple people while balancing speed and quality.

The main theoretical insight is that adaptive hiring rules can improve quality over time, but no strategy escapes the basic trade-off:

* stricter rules produce better employees but slower hiring,
* looser rules produce faster hiring but lower long-term quality,
* mean- and median-based rules offer mathematically analyzable compromises.

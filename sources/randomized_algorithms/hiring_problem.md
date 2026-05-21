# The Hiring Problem: Going Beyond Secretaries

## Sources

This summary is based on the slide deck **"The Hiring Problem: Going Beyond Secretaries"**, available at:

<https://theory.stanford.edu/~sergei/slides/hiring-dagstuhl.pdf>

The title slide lists Sergei Vassilvitskii, Andrei Broder, Adam Kirsch, Ravi Kumar, Michael Mitzenmacher, and Eli Upfal, with affiliations at Yahoo!, Harvard, and Brown.

---

## 1. Classical Secretary Problem

The classical **secretary problem** studies sequential decision-making under uncertainty.

### Problem Setup

- There are `n` candidates.
- Candidates are interviewed one at a time.
- After each interview, the decision-maker must either accept the candidate or reject the candidate permanently.
- The goal is to maximize the probability of selecting the single best candidate.

The problem is less about secretaries and more about **optimal stopping**: deciding when to stop observing and commit to the current option.

---

## 2. From Secretary Selection to Hiring

The deck generalizes the classical secretary problem to a more realistic hiring situation.

Instead of hiring exactly one person, imagine a growing organization that needs to hire many employees. It wants good employees, but it cannot wait indefinitely for perfect candidates.

### Central Trade-Off

The hiring problem studies the trade-off between:

- the number of interviews required,
- the number of people hired,
- the average quality of the hired employees.

This turns the problem from "choose the best single candidate" into a repeated online hiring process.

---

## 3. Hiring Model

The model used in the slides is deliberately simple.

### Assumptions

- Candidates arrive one at a time.
- Each candidate has an independent quality score.
- Candidate quality is modeled as `q_i ~ Uniform(0, 1)`.
- During each interview, the candidate's quality score is observed.
- The decision-maker chooses whether to hire or reject the candidate.

The slides note that other distributions can be handled, but the talk focuses on the uniform case.

---

## 4. Basic Hiring Strategies

The slides compare several simple online hiring strategies.

### Fixed Threshold Hiring

Set a fixed threshold `t`.

Hire candidate `i` if `q_i >= t`.

This is simple, but the expected quality does not improve over time. For threshold `t`:

- hiring rate is `1 - t`;
- average quality approaches `(1 + t) / 2`.

The organization reaches a fixed quality level, but quality stagnates.

### Maximum Hiring

Hire a candidate only if the candidate is better than everyone already hired.

This produces high-quality employees, because each new hire improves the current maximum. However, the process becomes increasingly slow as quality approaches 1.

If `g_i = 1 - q_i` is the gap between perfect quality and the current hire's quality, then after a new maximum:

`E[g_i | g_(i-1)] = g_(i-1) / 2`.

The qualitative conclusion is:

- quality improves quickly;
- hiring becomes extremely slow.

---

## 5. Lake Wobegon Strategies

The slides introduce **Lake Wobegon strategies**, named after the joke that everyone is "above average."

The idea is to hire candidates who are above the current average level of the organization. The slides consider two variants:

1. hire above the mean;
2. hire above the median.

These strategies are more adaptive than fixed threshold hiring because the hiring standard rises as the organization improves.

---

## 6. Hiring Above the Mean

In the **above-mean** strategy:

- start with an employee of quality `q`;
- after each hire, compute the current mean quality;
- hire the next candidate whose score is above that mean.

The slides analyze the quality gap and show that after `n` hires, average quality approaches:

`1 - Theta(1 / sqrt(n))`.

The time required to hire `n` employees is approximately:

`Theta(n^(3/2))`.

### Interpretation

Hiring above the mean gives a reasonable compromise:

- quality improves over time;
- hiring is much faster than maximum hiring;
- quality improves only at a `1 / sqrt(n)` rate.

---

## 7. Hiring Above the Median

In the **above-median** strategy:

- maintain an odd number of employees, written as `2k + 1`;
- compute the median employee quality;
- hire candidates whose quality is above the current median.

### Main Results

The median quality after `n` hires improves roughly as:

`1 - 1/n`.

The mean gap behaves like:

`Theta(log(n) / n)`.

The time required to hire `n` employees is:

`Theta(n^2)`.

### Interpretation

Hiring above the median produces stronger quality improvement than hiring above the mean, but it requires more interviews.

---

## 8. Comparison of Strategies

| Strategy | Rule | Quality behavior | Hiring speed | Main weakness |
|---|---|---:|---:|---|
| Fixed threshold | Hire if `q_i >= t` | Approaches `(1 + t) / 2` | Constant-rate hiring | Quality stagnates |
| Maximum hiring | Hire only if better than all previous hires | Very high quality | Extremely slow | Too few hires |
| Above mean | Hire if above current mean | `1 - Theta(1 / sqrt(n))` | `Theta(n^(3/2))` time for `n` hires | Weak concentration |
| Above median | Hire if above current median | Mean gap `Theta(log(n) / n)` | `Theta(n^2)` time for `n` hires | Slower hiring |

---

## 9. Extensions Mentioned in the Slides

The final slides mention several possible extensions:

- interview preprocessing;
- self-selection, where applicant quality may increase over time;
- noisy estimates of candidate scores;
- firing policies, such as periodically firing the bottom 10%;
- median-based firing and replacement strategies.

---

## 10. Core Takeaway

The classical secretary problem is too narrow for realistic hiring. Real organizations often need to hire multiple people while balancing speed and quality.

The main theoretical insight is that adaptive hiring rules can improve quality over time, but no strategy escapes the basic trade-off:

- stricter rules produce better employees but slower hiring;
- looser rules produce faster hiring but lower long-term quality;
- mean- and median-based rules offer mathematically analyzable compromises.

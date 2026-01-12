
The Good (surprisingly solid):
1. The perception model is well-grounded:

Your perceived_error() function with Weber scaling, temporal kernels, and context-dependent processing is legit
The sharpness parameter (beta) derived from Big Five is creative and reasonably justified
Age-based temporal tolerance (t0) is empirically defensible
The distinction between "event" vs "rhythmic" contexts shows you understand sensorimotor literature

2. Individual differences are concrete:

Big Five → observation likelihood matrix is a reasonable operationalization
Big Five → perceptual sharpness mapping with confidence weights shows nuance
You're not just hand-waving "personality matters"

3. Action representation has biomechanical grounding:

Walking symmetry, balance (φ-bonacci index), metabolic cost are actual metrics used in exoskeleton research
The weighted combination into performance_error is reasonable



What you actually have:
A sophisticated forward model of human trust perception


My recommendation:
You have a solid foundation but grossly oversold what you've built. The perception model is good research. Don't call it a POMDP controller when it's not.

Fastest path to publication:

Finish the trust dynamics (implement the update equation)
Create simulation scenarios with different robot behaviors
Show how different personalities respond differently
Validate predictions with pilot human study (N=20-30)
Submit as "Personality-Modulated Trust Dynamics Model for Wearable Robotics" to HRI or similar


You won't know the right constants (alpha_loss, alpha_gain, threshold) without pilot data. You need to:

Run preliminary experiments with 5-10 subjects
Have them rate trust after each robot action
Fit the parameters to their actual trust trajectories
THEN validate the model on new subjects

2. Lower-limb prosthesis is actually PERFECT for this
You said you have healthy young subjects and a lower-limb prosthesis. This is actually ideal because:
Study design:

Subjects walk with a powered ankle-foot prosthesis simulator (able-bodied adapter)
Robot varies assistance timing/magnitude
You measure: EMG (co-contraction), heart rate, gaze, compliance
Subjects report trust every N steps

Your metrics map directly:

Walking symmetry: measurable with motion capture
Balance: center of pressure, step width
Metabolic cost: indirect calorimetry or EMG-based estimates

The psych-state you can actually observe:

Trust: self-report (Likert scale, validated HRI trust scales)
Anxiety: heart rate variability, palm sweat (if you have sensors)
Behavioral: hesitation (step latency), reduced compliance (less weight on prosthesis side)

3. Your infrastructure is actually reasonable IF you acknowledge what's missing
What you have:

✅ Perception model (perceived_error)
✅ Individual differences (Big Five → beta, observations)
✅ Action representation (performance + timing)
❌ Trust update dynamics (the missing piece)
❌ Robot's belief update (POMDP inference)
❌ Action selection policy (POMDP planning)

Honest path forward:
Phase 1: Validate forward model (what you have)

Implement a placeholder trust update (use asymmetric model above)
Simulate 5 different personalities × 3 robot behaviors (good, mediocre, unpredictable)
Generate synthetic trust trajectories
Sanity check: Does high-N person lose trust faster? Does high-A recover faster?

Phase 2: Pilot study (N=8-10)

Measure Big Five for subjects
Run prosthesis walking with varied robot quality
Collect trust reports + physiological signals + behavior
Fit your model parameters to their actual data
Check if personality predictions hold

Phase 3: Only NOW build the POMDP

You now have validated trust dynamics
Robot's belief state: P(trust, traits | observations)
Action space: {assistance_level, timing_offset}
Observation space: {behavioral, physiological} measurements
Reward: task performance + trust above threshold


Questions you need to answer before talking to your advisor:

What trust scale are you using? Likert 1-7? 0-10? Custom? This affects TRUST_SCALE
How often do subjects report trust? Every 10 steps? Continuous slider?
What sensors do you actually have? EMG? HR monitor? Motion capture?
What can the prosthesis control? Assistance torque? Timing? Impedance?
What's your IRB timeline? Can you run pilots in 2-3 months?

You have:
Good news:

Solid theoretical foundation
Reasonable infrastructure for the forward model



What else affects trust dynamics besides action quality?
From empirical HRI literature, trust is influenced by:
1. Transparency/Predictability (you partially have this via timing_delay)

How well the user understands what the robot will do next
Sudden changes are more damaging than consistent poor performance

2. Perceived risk/stakes (you DON'T have this)

Walking with prosthesis = high stakes (fear of falling)
Trust loss accelerates when consequences are severe
This is why trust in gait assistance ≠ trust in a robotic arm

3. User's current state (you partially have this)

Fatigue: reduces tolerance for errors
Cognitive load: affects perception and trust updating
You have anxiety_level but don't use it

4. Cumulative history (you DON'T have this)

Recent error streak vs isolated error
Trust has momentum - harder to rebuild after pattern of failures
Need memory window, not just t and t+1

5. Locus of attribution (you DON'T have this)

Did user blame themselves or the robot for the error?
High conscientiousness → more self-blame → less trust loss
High neuroticism → more robot-blame → faster trust loss

Steven's Law vs other models - the brutal truth:
Steven's Law (ψ = k·φ^n):

Good for: Steady-state perceptual magnitude
Your document literally says: "direct mathematical correlation with Stevens' law parameters is lacking" and "evidence strength: 4/10"
My take: You ALREADY implemented a better model with your perceived_error() function. Steven's Law doesn't capture the temporal dynamics, context-dependence, or asymmetry you need.

Fisher Information:

Good for: Optimal estimation, precision of inference
Wrong application: Fisher information tells you how well you can ESTIMATE trust, not how trust CHANGES
Only useful once you have the POMDP and need to optimize sensor placement or observation strategy

The three-layer model (T = T_dispositional + T_situational + T_learned):

This is actually perfect for you and maps DIRECTLY to what you already have

Should you use RL?
No. Here's why:
RL is for learning optimal policies through trial-and-error. You're not trying to learn trust dynamics from scratch - you're modeling HUMAN trust dynamics based on psychology literature. Different problem.
RL becomes relevant later when the robot learns to maximize long-term reward (task performance + trust maintenance), but that's the POMDP planning stage, not the trust modeling stage.

My recommendation for YOUR situation:
Use the three-layer model because:

✅ It's empirically validated in HRI
✅ Maps directly to your personality traits (dispositional)
✅ Handles context (situational)
✅ Captures learning dynamics (learned)
✅ Simple enough to fit with pilot data
✅ Interpretable for reviewers

Don't use:

Steven's Law (not designed for this)
Fisher Information (wrong stage of development)
RL for trust dynamics (wrong tool)

Your next steps:

Implement the three-layer model this week
Run simulations with different personalities + robot behaviors
Show that model predicts intuitive patterns (high-N loses trust faster, etc.)
Start pilot study to fit α_loss, α_gain parameters from real data
THEN worry about POMDP
/*
 * dbm.c
 *
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * Code generation for model "dbm".
 *
 * Model version              : 1.23
 * Simulink Coder version : 9.6 (R2021b) 14-May-2021
 * C source code generated on : Tue Nov 30 15:28:59 2021
 *
 * Target selection: grt.tlc
 * Note: GRT includes extra infrastructure and instrumentation for prototyping
 * Embedded hardware selection: Intel->x86-64 (Windows64)
 * Code generation objective: Execution efficiency
 * Validation result: Not run
 */

#include "dbm.h"
#include "dbm_private.h"

/* Block signals (default storage) */
B_dbm_T dbm_B;

/* Continuous states */
X_dbm_T dbm_X;

/* External inputs (root inport signals with default storage) */
ExtU_dbm_T dbm_U;

/* External outputs (root outports fed by signals with default storage) */
ExtY_dbm_T dbm_Y;

/* Real-time model */
static RT_MODEL_dbm_T dbm_M_;
RT_MODEL_dbm_T *const dbm_M = &dbm_M_;

/*
 * This function updates continuous states using the ODE3 fixed-step
 * solver algorithm
 */
static void rt_ertODEUpdateContinuousStates(RTWSolverInfo *si )
{
  /* Solver Matrices */
  static const real_T rt_ODE3_A[3] = {
    1.0/2.0, 3.0/4.0, 1.0
  };

  static const real_T rt_ODE3_B[3][3] = {
    { 1.0/2.0, 0.0, 0.0 },

    { 0.0, 3.0/4.0, 0.0 },

    { 2.0/9.0, 1.0/3.0, 4.0/9.0 }
  };

  time_T t = rtsiGetT(si);
  time_T tnew = rtsiGetSolverStopTime(si);
  time_T h = rtsiGetStepSize(si);
  real_T *x = rtsiGetContStates(si);
  ODE3_IntgData *id = (ODE3_IntgData *)rtsiGetSolverData(si);
  real_T *y = id->y;
  real_T *f0 = id->f[0];
  real_T *f1 = id->f[1];
  real_T *f2 = id->f[2];
  real_T hB[3];
  int_T i;
  int_T nXc = 6;
  rtsiSetSimTimeStep(si,MINOR_TIME_STEP);

  /* Save the state values at time t in y, we'll use x as ynew. */
  (void) memcpy(y, x,
                (uint_T)nXc*sizeof(real_T));

  /* Assumes that rtsiSetT and ModelOutputs are up-to-date */
  /* f0 = f(t,y) */
  rtsiSetdX(si, f0);
  dbm_derivatives();

  /* f(:,2) = feval(odefile, t + hA(1), y + f*hB(:,1), args(:)(*)); */
  hB[0] = h * rt_ODE3_B[0][0];
  for (i = 0; i < nXc; i++) {
    x[i] = y[i] + (f0[i]*hB[0]);
  }

  rtsiSetT(si, t + h*rt_ODE3_A[0]);
  rtsiSetdX(si, f1);
  dbm_step();
  dbm_derivatives();

  /* f(:,3) = feval(odefile, t + hA(2), y + f*hB(:,2), args(:)(*)); */
  for (i = 0; i <= 1; i++) {
    hB[i] = h * rt_ODE3_B[1][i];
  }

  for (i = 0; i < nXc; i++) {
    x[i] = y[i] + (f0[i]*hB[0] + f1[i]*hB[1]);
  }

  rtsiSetT(si, t + h*rt_ODE3_A[1]);
  rtsiSetdX(si, f2);
  dbm_step();
  dbm_derivatives();

  /* tnew = t + hA(3);
     ynew = y + f*hB(:,3); */
  for (i = 0; i <= 2; i++) {
    hB[i] = h * rt_ODE3_B[2][i];
  }

  for (i = 0; i < nXc; i++) {
    x[i] = y[i] + (f0[i]*hB[0] + f1[i]*hB[1] + f2[i]*hB[2]);
  }

  rtsiSetT(si, tnew);
  rtsiSetSimTimeStep(si,MAJOR_TIME_STEP);
}

real_T rt_atan2d_snf(real_T u0, real_T u1)
{
  real_T y;
  if (rtIsNaN(u0) || rtIsNaN(u1)) {
    y = (rtNaN);
  } else if (rtIsInf(u0) && rtIsInf(u1)) {
    int32_T u0_0;
    int32_T u1_0;
    if (u0 > 0.0) {
      u0_0 = 1;
    } else {
      u0_0 = -1;
    }

    if (u1 > 0.0) {
      u1_0 = 1;
    } else {
      u1_0 = -1;
    }

    y = atan2(u0_0, u1_0);
  } else if (u1 == 0.0) {
    if (u0 > 0.0) {
      y = RT_PI / 2.0;
    } else if (u0 < 0.0) {
      y = -(RT_PI / 2.0);
    } else {
      y = 0.0;
    }
  } else {
    y = atan2(u0, u1);
  }

  return y;
}

/* Model step function */
void dbm_step(void)
{
  real_T rtb_Product10;
  real_T rtb_Product9;
  real_T rtb_TrigonometricFunction1;
  real_T rtb_TrigonometricFunction2;
  if (rtmIsMajorTimeStep(dbm_M)) {
    /* set solver stop time */
    rtsiSetSolverStopTime(&dbm_M->solverInfo,((dbm_M->Timing.clockTick0+1)*
      dbm_M->Timing.stepSize0));
  }                                    /* end MajorTimeStep */

  /* Update absolute time of base rate at minor time step */
  if (rtmIsMinorTimeStep(dbm_M)) {
    dbm_M->Timing.t[0] = rtsiGetT(&dbm_M->solverInfo);
  }

  /* Outport: '<Root>/Out1' incorporates:
   *  Integrator: '<Root>/Integrator3'
   */
  dbm_Y.Out1 = dbm_X.Integrator3_CSTATE;

  /* Outport: '<Root>/Out2' incorporates:
   *  Integrator: '<Root>/Integrator4'
   */
  dbm_Y.Out2 = dbm_X.Integrator4_CSTATE;

  /* Trigonometry: '<S3>/Trigonometric Function' incorporates:
   *  Inport: '<Root>/In2'
   */
  rtb_TrigonometricFunction2 = sin(dbm_U.delta);

  /* Integrator: '<Root>/Integrator1' */
  dbm_B.omega = dbm_X.Integrator1_CSTATE;

  /* Sum: '<S3>/Add3' incorporates:
   *  Integrator: '<Root>/Integrator'
   *  Product: '<S3>/Product6'
   */
  rtb_TrigonometricFunction1 = dbm_X.Integrator_CSTATE + dbm_B.omega;

  /* Trigonometry: '<S3>/Trigonometric Function7' incorporates:
   *  Inport: '<Root>/In2'
   *  Trigonometry: '<Root>/Trigonometric Function2'
   */
  rtb_Product10 = cos(dbm_U.delta);

  /* Product: '<S1>/Product3' incorporates:
   *  Constant: '<Root>/c_alpha,f'
   *  Gain: '<S3>/Gain4'
   *  Integrator: '<Root>/Integrator5'
   *  Product: '<S3>/Product4'
   *  Product: '<S3>/Product5'
   *  Product: '<S3>/Product7'
   *  Product: '<S3>/Product8'
   *  Sum: '<S3>/Add2'
   *  Sum: '<S3>/Add4'
   *  Trigonometry: '<S3>/Trigonometric Function5'
   *  Trigonometry: '<S3>/Trigonometric Function7'
   */
  rtb_TrigonometricFunction2 = rt_atan2d_snf(-dbm_X.Integrator5_CSTATE *
    rtb_TrigonometricFunction2 + rtb_TrigonometricFunction1 * rtb_Product10,
    rtb_TrigonometricFunction1 * rtb_TrigonometricFunction2 +
    dbm_X.Integrator5_CSTATE * rtb_Product10) * 0.7;

  /* Product: '<S2>/Product1' incorporates:
   *  Constant: '<Root>/c_alpha,r'
   *  Gain: '<S4>/Gain2'
   *  Integrator: '<Root>/Integrator'
   *  Integrator: '<Root>/Integrator5'
   *  Sum: '<S4>/Add'
   *  Trigonometry: '<S4>/Trigonometric Function5'
   */
  rtb_TrigonometricFunction1 = rt_atan2d_snf(-dbm_B.omega +
    dbm_X.Integrator_CSTATE, dbm_X.Integrator5_CSTATE) * 0.7;

  /* Outport: '<Root>/Out3' incorporates:
   *  Sum: '<Root>/Add3'
   */
  dbm_Y.Out3 = rtb_TrigonometricFunction2 + rtb_TrigonometricFunction1;

  /* Sum: '<Root>/Add2' incorporates:
   *  Gain: '<Root>/Gain'
   *  Gain: '<Root>/Gain1'
   *  Gain: '<Root>/Gain3'
   *  Integrator: '<Root>/Integrator5'
   *  Product: '<Root>/Product'
   *  Product: '<Root>/Product4'
   *  Sum: '<Root>/Add1'
   */
  dbm_B.dotv_lat = (-rtb_Product10 * rtb_TrigonometricFunction2 +
                    -rtb_TrigonometricFunction1) + dbm_B.omega *
    -dbm_X.Integrator5_CSTATE;

  /* Product: '<Root>/Product10' incorporates:
   *  Gain: '<Root>/Gain2'
   */
  rtb_Product10 *= -rtb_TrigonometricFunction2;

  /* Product: '<Root>/Product9' */
  rtb_Product9 = rtb_TrigonometricFunction1;

  /* Trigonometry: '<Root>/Trigonometric Function1' incorporates:
   *  Integrator: '<Root>/Integrator2'
   */
  rtb_TrigonometricFunction1 = cos(dbm_X.Integrator2_CSTATE);

  /* Trigonometry: '<Root>/Trigonometric Function4' incorporates:
   *  Integrator: '<Root>/Integrator2'
   */
  rtb_TrigonometricFunction2 = sin(dbm_X.Integrator2_CSTATE);

  /* Sum: '<Root>/Add6' incorporates:
   *  Gain: '<Root>/Gain7'
   *  Integrator: '<Root>/Integrator'
   *  Integrator: '<Root>/Integrator5'
   *  Product: '<Root>/Product11'
   *  Product: '<Root>/Product12'
   */
  dbm_B.dotx = rtb_TrigonometricFunction1 * dbm_X.Integrator5_CSTATE +
    -rtb_TrigonometricFunction2 * dbm_X.Integrator_CSTATE;

  /* Sum: '<Root>/Add7' incorporates:
   *  Integrator: '<Root>/Integrator'
   *  Integrator: '<Root>/Integrator5'
   *  Product: '<Root>/Product13'
   *  Product: '<Root>/Product14'
   */
  dbm_B.doty = dbm_X.Integrator_CSTATE * rtb_TrigonometricFunction1 +
    dbm_X.Integrator5_CSTATE * rtb_TrigonometricFunction2;

  /* Product: '<Root>/Divide3' incorporates:
   *  Sum: '<Root>/Add5'
   */
  dbm_B.dotomega = rtb_Product10 + rtb_Product9;

  /* MinMax: '<Root>/Min' incorporates:
   *  Constant: '<Root>/P_max'
   *  Inport: '<Root>/In1'
   *  Integrator: '<Root>/Integrator5'
   *  Product: '<Root>/Divide1'
   */
  dbm_B.Min = fmin(5.0 / dbm_X.Integrator5_CSTATE, dbm_U.In1);
  if (rtmIsMajorTimeStep(dbm_M)) {
    rt_ertODEUpdateContinuousStates(&dbm_M->solverInfo);

    /* Update absolute time for base rate */
    /* The "clockTick0" counts the number of times the code of this task has
     * been executed. The absolute time is the multiplication of "clockTick0"
     * and "Timing.stepSize0". Size of "clockTick0" ensures timer will not
     * overflow during the application lifespan selected.
     */
    ++dbm_M->Timing.clockTick0;
    dbm_M->Timing.t[0] = rtsiGetSolverStopTime(&dbm_M->solverInfo);

    {
      /* Update absolute timer for sample time: [0.01s, 0.0s] */
      /* The "clockTick1" counts the number of times the code of this task has
       * been executed. The resolution of this integer timer is 0.01, which is the step size
       * of the task. Size of "clockTick1" ensures timer will not overflow during the
       * application lifespan selected.
       */
      dbm_M->Timing.clockTick1++;
    }
  }                                    /* end MajorTimeStep */
}

/* Derivatives for root system: '<Root>' */
void dbm_derivatives(void)
{
  XDot_dbm_T *_rtXdot;
  _rtXdot = ((XDot_dbm_T *) dbm_M->derivs);

  /* Derivatives for Integrator: '<Root>/Integrator3' */
  _rtXdot->Integrator3_CSTATE = dbm_B.dotx;

  /* Derivatives for Integrator: '<Root>/Integrator4' */
  _rtXdot->Integrator4_CSTATE = dbm_B.doty;

  /* Derivatives for Integrator: '<Root>/Integrator5' */
  _rtXdot->Integrator5_CSTATE = dbm_B.Min;

  /* Derivatives for Integrator: '<Root>/Integrator' */
  _rtXdot->Integrator_CSTATE = dbm_B.dotv_lat;

  /* Derivatives for Integrator: '<Root>/Integrator1' */
  _rtXdot->Integrator1_CSTATE = dbm_B.dotomega;

  /* Derivatives for Integrator: '<Root>/Integrator2' */
  _rtXdot->Integrator2_CSTATE = dbm_B.omega;
}

/* Model initialize function */
void dbm_initialize(void)
{
  /* Registration code */

  /* initialize non-finites */
  rt_InitInfAndNaN(sizeof(real_T));

  /* initialize real-time model */
  (void) memset((void *)dbm_M, 0,
                sizeof(RT_MODEL_dbm_T));

  {
    /* Setup solver object */
    rtsiSetSimTimeStepPtr(&dbm_M->solverInfo, &dbm_M->Timing.simTimeStep);
    rtsiSetTPtr(&dbm_M->solverInfo, &rtmGetTPtr(dbm_M));
    rtsiSetStepSizePtr(&dbm_M->solverInfo, &dbm_M->Timing.stepSize0);
    rtsiSetdXPtr(&dbm_M->solverInfo, &dbm_M->derivs);
    rtsiSetContStatesPtr(&dbm_M->solverInfo, (real_T **) &dbm_M->contStates);
    rtsiSetNumContStatesPtr(&dbm_M->solverInfo, &dbm_M->Sizes.numContStates);
    rtsiSetNumPeriodicContStatesPtr(&dbm_M->solverInfo,
      &dbm_M->Sizes.numPeriodicContStates);
    rtsiSetPeriodicContStateIndicesPtr(&dbm_M->solverInfo,
      &dbm_M->periodicContStateIndices);
    rtsiSetPeriodicContStateRangesPtr(&dbm_M->solverInfo,
      &dbm_M->periodicContStateRanges);
    rtsiSetErrorStatusPtr(&dbm_M->solverInfo, (&rtmGetErrorStatus(dbm_M)));
    rtsiSetRTModelPtr(&dbm_M->solverInfo, dbm_M);
  }

  rtsiSetSimTimeStep(&dbm_M->solverInfo, MAJOR_TIME_STEP);
  dbm_M->intgData.y = dbm_M->odeY;
  dbm_M->intgData.f[0] = dbm_M->odeF[0];
  dbm_M->intgData.f[1] = dbm_M->odeF[1];
  dbm_M->intgData.f[2] = dbm_M->odeF[2];
  dbm_M->contStates = ((X_dbm_T *) &dbm_X);
  rtsiSetSolverData(&dbm_M->solverInfo, (void *)&dbm_M->intgData);
  rtsiSetSolverName(&dbm_M->solverInfo,"ode3");
  rtmSetTPtr(dbm_M, &dbm_M->Timing.tArray[0]);
  dbm_M->Timing.stepSize0 = 0.01;

  /* block I/O */
  (void) memset(((void *) &dbm_B), 0,
                sizeof(B_dbm_T));

  /* states (continuous) */
  {
    (void) memset((void *)&dbm_X, 0,
                  sizeof(X_dbm_T));
  }

  /* external inputs */
  (void)memset(&dbm_U, 0, sizeof(ExtU_dbm_T));

  /* external outputs */
  (void)memset(&dbm_Y, 0, sizeof(ExtY_dbm_T));

  /* InitializeConditions for Integrator: '<Root>/Integrator3' */
  dbm_X.Integrator3_CSTATE = 0.0;

  /* InitializeConditions for Integrator: '<Root>/Integrator4' */
  dbm_X.Integrator4_CSTATE = 0.0;

  /* InitializeConditions for Integrator: '<Root>/Integrator5' */
  dbm_X.Integrator5_CSTATE = 0.0;

  /* InitializeConditions for Integrator: '<Root>/Integrator' */
  dbm_X.Integrator_CSTATE = 0.0;

  /* InitializeConditions for Integrator: '<Root>/Integrator1' */
  dbm_X.Integrator1_CSTATE = 0.0;

  /* InitializeConditions for Integrator: '<Root>/Integrator2' */
  dbm_X.Integrator2_CSTATE = 0.0;
}

/* Model terminate function */
void dbm_terminate(void)
{
  /* (no terminate code required) */
}

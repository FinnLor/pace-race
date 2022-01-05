/*
 * rtwdemo_secondOrderSystem_data.c
 *
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * Code generation for model "rtwdemo_secondOrderSystem".
 *
 * Model version              : 4.1
 * Simulink Coder version : 9.6 (R2021b) 14-May-2021
 * C source code generated on : Mon Nov 29 20:00:42 2021
 *
 * Target selection: grt.tlc
 * Note: GRT includes extra infrastructure and instrumentation for prototyping
 * Embedded hardware selection: Intel->x86-64 (Windows64)
 * Code generation objective: Debugging
 * Validation result: Not run
 */

#include "rtwdemo_secondOrderSystem.h"
#include "rtwdemo_secondOrderSystem_private.h"

/* Block parameters (default storage) */
P_rtwdemo_secondOrderSystem_T rtwdemo_secondOrderSystem_P = {
  /* Expression: 4
   * Referenced by: '<Root>/Force: f(t)'
   */
  4.0,

  /* Expression: 20
   * Referenced by: '<Root>/Force: f(t)'
   */
  20.0,

  /* Expression: 0
   * Referenced by: '<Root>/Integrator2'
   */
  0.0,

  /* Expression: 0
   * Referenced by: '<Root>/Integrator1'
   */
  0.0,

  /* Expression: 397.0116577148438
   * Referenced by: '<Root>/Damping'
   */
  397.01165771484381,

  /* Expression: 1000000
   * Referenced by: '<Root>/Stiffness'
   */
  1.0E+6,

  /* Expression: 1000000
   * Referenced by: '<Root>/Mass'
   */
  1.0E+6
};

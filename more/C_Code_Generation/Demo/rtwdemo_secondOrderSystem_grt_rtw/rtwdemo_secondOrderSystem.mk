###########################################################################
## Makefile generated for component 'rtwdemo_secondOrderSystem'. 
## 
## Makefile     : rtwdemo_secondOrderSystem.mk
## Generated on : Mon Nov 29 20:18:51 2021
## Final product: $(RELATIVE_PATH_TO_ANCHOR)\rtwdemo_secondOrderSystem.exe
## Product type : executable
## 
###########################################################################

###########################################################################
## MACROS
###########################################################################

# Macro Descriptions:
# PRODUCT_NAME            Name of the system to build
# MAKEFILE                Name of this makefile
# COMPILER_COMMAND_FILE   Compiler command listing model reference header paths
# CMD_FILE                Command file

PRODUCT_NAME              = rtwdemo_secondOrderSystem
MAKEFILE                  = rtwdemo_secondOrderSystem.mk
MATLAB_ROOT               = C:\PROGRA~1\MATLAB\R2021b
MATLAB_BIN                = C:\PROGRA~1\MATLAB\R2021b\bin
MATLAB_ARCH_BIN           = $(MATLAB_BIN)\win64
START_DIR                 = C:\Users\felix\sciebo2\OKS
SOLVER                    = 
SOLVER_OBJ                = 
CLASSIC_INTERFACE         = 0
TGT_FCN_LIB               = None
MODEL_HAS_DYNAMICALLY_LOADED_SFCNS = 0
RELATIVE_PATH_TO_ANCHOR   = ..
COMPILER_COMMAND_FILE     = rtwdemo_secondOrderSystem_comp.rsp
CMD_FILE                  = rtwdemo_secondOrderSystem.rsp
C_STANDARD_OPTS           = 
CPP_STANDARD_OPTS         = 
NODEBUG                   = 1

###########################################################################
## TOOLCHAIN SPECIFICATIONS
###########################################################################

# Toolchain Name:          Microsoft Visual C++ 2019 v16.0 | nmake (64-bit Windows)
# Supported Version(s):    16.0
# ToolchainInfo Version:   2021b
# Specification Revision:  1.0
# 
#-------------------------------------------
# Macros assumed to be defined elsewhere
#-------------------------------------------

# NODEBUG
# cvarsdll
# cvarsmt
# conlibsmt
# ldebug
# conflags
# cflags

#-----------
# MACROS
#-----------

MW_EXTERNLIB_DIR    = $(MATLAB_ROOT)\extern\lib\win64\microsoft
MW_LIB_DIR          = $(MATLAB_ROOT)\lib\win64
CPU                 = AMD64
APPVER              = 5.02
CVARSFLAG           = $(cvarsmt)
CFLAGS_ADDITIONAL   = -D_CRT_SECURE_NO_WARNINGS
CPPFLAGS_ADDITIONAL = -EHs -D_CRT_SECURE_NO_WARNINGS /wd4251
LIBS_TOOLCHAIN      = $(conlibs)

TOOLCHAIN_SRCS = 
TOOLCHAIN_INCS = 
TOOLCHAIN_LIBS = 

#------------------------
# BUILD TOOL COMMANDS
#------------------------

# C Compiler: Microsoft Visual C Compiler
CC = cl

# Linker: Microsoft Visual C Linker
LD = link

# C++ Compiler: Microsoft Visual C++ Compiler
CPP = cl

# C++ Linker: Microsoft Visual C++ Linker
CPP_LD = link

# Archiver: Microsoft Visual C/C++ Archiver
AR = lib

# MEX Tool: MEX Tool
MEX_PATH = $(MATLAB_ARCH_BIN)
MEX = "$(MEX_PATH)\mex"

# Download: Download
DOWNLOAD =

# Execute: Execute
EXECUTE = $(PRODUCT)

# Builder: NMAKE Utility
MAKE = nmake


#-------------------------
# Directives/Utilities
#-------------------------

CDEBUG              = -Zi
C_OUTPUT_FLAG       = -Fo
LDDEBUG             = /DEBUG
OUTPUT_FLAG         = -out:
CPPDEBUG            = -Zi
CPP_OUTPUT_FLAG     = -Fo
CPPLDDEBUG          = /DEBUG
OUTPUT_FLAG         = -out:
ARDEBUG             =
STATICLIB_OUTPUT_FLAG = -out:
MEX_DEBUG           = -g
RM                  = @del
ECHO                = @echo
MV                  = @ren
RUN                 = @cmd /C

#----------------------------------------
# "Faster Builds" Build Configuration
#----------------------------------------

MEX_CPPFLAGS         =
MEX_CPPLDFLAGS       =
MEX_CFLAGS           =
MEX_LDFLAGS          =



#---------------------------
# Model-Specific Options
#---------------------------

CFLAGS = $(cflags) $(CVARSFLAG) $(CFLAGS_ADDITIONAL) /Od /Oy- $(CDEBUG) -Zi

LDFLAGS = $(ldebug) $(conflags) $(LIBS_TOOLCHAIN) $(LDDEBUG) /DEBUG

SHAREDLIB_LDFLAGS = $(ldebug) $(conflags) $(LIBS_TOOLCHAIN) -dll -def:$(DEF_FILE) $(LDDEBUG) /DEBUG

CPPFLAGS = /TP $(cflags) $(CVARSFLAG) $(CPPFLAGS_ADDITIONAL) /Od /Oy- $(CPPDEBUG) -Zi

CPP_LDFLAGS = $(ldebug) $(conflags) $(LIBS_TOOLCHAIN) $(LDDEBUG) /DEBUG

CPP_SHAREDLIB_LDFLAGS = $(ldebug) $(conflags) $(LIBS_TOOLCHAIN) -dll -def:$(DEF_FILE) $(LDDEBUG) /DEBUG

ARFLAGS = /nologo $(ARDEBUG)

DOWNLOAD_FLAGS = 

EXECUTE_FLAGS = 

MAKE_FLAGS = -f $(MAKEFILE)

###########################################################################
## OUTPUT INFO
###########################################################################

PRODUCT = $(RELATIVE_PATH_TO_ANCHOR)\rtwdemo_secondOrderSystem.exe
PRODUCT_TYPE = "executable"
BUILD_TYPE = "Top-Level Standalone Executable"

###########################################################################
## INCLUDE PATHS
###########################################################################

INCLUDES_BUILDINFO = 

INCLUDES = $(INCLUDES_BUILDINFO)

###########################################################################
## DEFINES
###########################################################################

DEFINES_BUILD_ARGS = -DCLASSIC_INTERFACE=0 -DALLOCATIONFCN=0 -DEXT_MODE=1 -DMAT_FILE=0 -DONESTEPFCN=1 -DTERMFCN=1 -DMULTI_INSTANCE_CODE=0 -DINTEGER_CODE=0 -DMT=0
DEFINES_CUSTOM = 
DEFINES_OPTS = -DXCP_DAQ_SUPPORT -DXCP_CALIBRATION_SUPPORT -DXCP_TIMESTAMP_SUPPORT -DXCP_TIMESTAMP_BASED_ON_SIMULATION_TIME -DXCP_SET_MTA_SUPPORT -DXCP_MEM_DAQ_RESERVED_POOLS_NUMBER=2 -DEXTMODE_XCP_TRIGGER_SUPPORT -DXCP_EXTMODE_RUN_BACKGROUND_FLUSH -DEXTMODE_STATIC -DEXTMODE_STATIC_SIZE=1000000 -DON_TARGET_WAIT_FOR_START=0 -DTID01EQ=1
DEFINES_STANDARD = -DMODEL=rtwdemo_secondOrderSystem -DNUMST=2 -DNCSTATES=2 -DHAVESTDIO -DRT -DUSE_RTMODEL

DEFINES = $(DEFINES_BUILD_ARGS) $(DEFINES_CUSTOM) $(DEFINES_OPTS) $(DEFINES_STANDARD)

###########################################################################
## SOURCE FILES
###########################################################################

SRCS = xcp_ext_work.c $(START_DIR)\rtwdemo_secondOrderSystem_grt_rtw\rtwdemo_secondOrderSystem.c $(START_DIR)\rtwdemo_secondOrderSystem_grt_rtw\rtwdemo_secondOrderSystem_data.c $(MATLAB_ROOT)\toolbox\coder\xcp\src\target\ext_mode\src\xcp_ext_common.c $(MATLAB_ROOT)\toolbox\coder\xcp\src\target\ext_mode\src\xcp_ext_classic_trigger.c $(MATLAB_ROOT)\toolbox\coder\xcp\src\target\slave\protocol\src\xcp.c $(MATLAB_ROOT)\toolbox\coder\xcp\src\target\slave\protocol\src\xcp_standard.c $(MATLAB_ROOT)\toolbox\coder\xcp\src\target\slave\protocol\src\xcp_daq.c $(MATLAB_ROOT)\toolbox\coder\xcp\src\target\slave\protocol\src\xcp_calibration.c $(MATLAB_ROOT)\toolbox\coder\xcp\src\target\slave\transport\src\xcp_fifo.c $(MATLAB_ROOT)\toolbox\coder\xcp\src\target\slave\transport\src\xcp_transport.c $(MATLAB_ROOT)\toolbox\coder\xcp\src\target\slave\platform\default\xcp_mem_default.c $(MATLAB_ROOT)\toolbox\coder\xcp\src\target\slave\platform\default\xcp_drv_rtiostream.c $(MATLAB_ROOT)\toolbox\coder\xcp\src\target\slave\transport\src\xcp_frame_tcp.c $(MATLAB_ROOT)\toolbox\coder\xcp\src\target\ext_mode\src\xcp_ext_param_default_tcp.c $(MATLAB_ROOT)\toolbox\coder\xcp\src\target\slave\platform\default\xcp_platform_default.c $(MATLAB_ROOT)\toolbox\coder\rtiostream\src\rtiostreamtcpip\rtiostream_tcpip.c

MAIN_SRC = $(MATLAB_ROOT)\rtw\c\src\common\rt_main.c

ALL_SRCS = $(SRCS) $(MAIN_SRC)

###########################################################################
## OBJECTS
###########################################################################

OBJS = xcp_ext_work.obj rtwdemo_secondOrderSystem.obj rtwdemo_secondOrderSystem_data.obj xcp_ext_common.obj xcp_ext_classic_trigger.obj xcp.obj xcp_standard.obj xcp_daq.obj xcp_calibration.obj xcp_fifo.obj xcp_transport.obj xcp_mem_default.obj xcp_drv_rtiostream.obj xcp_frame_tcp.obj xcp_ext_param_default_tcp.obj xcp_platform_default.obj rtiostream_tcpip.obj

MAIN_OBJ = rt_main.obj

ALL_OBJS = $(OBJS) $(MAIN_OBJ)

###########################################################################
## PREBUILT OBJECT FILES
###########################################################################

PREBUILT_OBJS = 

###########################################################################
## LIBRARIES
###########################################################################

LIBS = $(START_DIR)\slprj\grt\_sharedutils\rtwshared.lib

###########################################################################
## SYSTEM LIBRARIES
###########################################################################

SYSTEM_LIBS = 

###########################################################################
## ADDITIONAL TOOLCHAIN FLAGS
###########################################################################

#---------------
# C Compiler
#---------------

CFLAGS_BASIC = $(DEFINES) @$(COMPILER_COMMAND_FILE)

CFLAGS = $(CFLAGS) $(CFLAGS_BASIC)

#-----------------
# C++ Compiler
#-----------------

CPPFLAGS_BASIC = $(DEFINES) @$(COMPILER_COMMAND_FILE)

CPPFLAGS = $(CPPFLAGS) $(CPPFLAGS_BASIC)

###########################################################################
## INLINED COMMANDS
###########################################################################


!include $(MATLAB_ROOT)\rtw\c\tools\vcdefs.mak


###########################################################################
## PHONY TARGETS
###########################################################################

.PHONY : all build buildobj clean info prebuild download execute set_environment_variables


all : build
	@cmd /C "@echo ### Successfully generated all binary outputs."


build : set_environment_variables prebuild $(PRODUCT)


buildobj : set_environment_variables prebuild $(OBJS) $(PREBUILT_OBJS) $(LIBS)
	@cmd /C "@echo ### Successfully generated all binary outputs."


prebuild : 


download : $(PRODUCT)


execute : download
	@cmd /C "@echo ### Invoking postbuild tool "Execute" ..."
	$(EXECUTE) $(EXECUTE_FLAGS)
	@cmd /C "@echo ### Done invoking postbuild tool."


set_environment_variables : 
	@set INCLUDE=$(INCLUDES);$(INCLUDE)
	@set LIB=$(LIB)


###########################################################################
## FINAL TARGET
###########################################################################

#-------------------------------------------
# Create a standalone executable            
#-------------------------------------------

$(PRODUCT) : $(OBJS) $(PREBUILT_OBJS) $(LIBS) $(MAIN_OBJ)
	@cmd /C "@echo ### Creating standalone executable "$(PRODUCT)" ..."
	$(LD) $(LDFLAGS) -out:$(PRODUCT) @$(CMD_FILE) $(LIBS) $(SYSTEM_LIBS) $(TOOLCHAIN_LIBS)
	@cmd /C "@echo ### Created: $(PRODUCT)"


###########################################################################
## INTERMEDIATE TARGETS
###########################################################################

#---------------------
# SOURCE-TO-OBJECT
#---------------------

.c.obj :
	$(CC) $(CFLAGS) -Fo"$@" "$<"


.cpp.obj :
	$(CPP) $(CPPFLAGS) -Fo"$@" "$<"


{$(RELATIVE_PATH_TO_ANCHOR)}.c.obj :
	$(CC) $(CFLAGS) -Fo"$@" "$<"


{$(RELATIVE_PATH_TO_ANCHOR)}.cpp.obj :
	$(CPP) $(CPPFLAGS) -Fo"$@" "$<"


{$(START_DIR)}.c.obj :
	$(CC) $(CFLAGS) -Fo"$@" "$<"


{$(START_DIR)}.cpp.obj :
	$(CPP) $(CPPFLAGS) -Fo"$@" "$<"


{$(START_DIR)\rtwdemo_secondOrderSystem_grt_rtw}.c.obj :
	$(CC) $(CFLAGS) -Fo"$@" "$<"


{$(START_DIR)\rtwdemo_secondOrderSystem_grt_rtw}.cpp.obj :
	$(CPP) $(CPPFLAGS) -Fo"$@" "$<"


{$(MATLAB_ROOT)\rtw\c\src}.c.obj :
	$(CC) $(CFLAGS) -Fo"$@" "$<"


{$(MATLAB_ROOT)\rtw\c\src}.cpp.obj :
	$(CPP) $(CPPFLAGS) -Fo"$@" "$<"


{$(MATLAB_ROOT)\simulink\src}.c.obj :
	$(CC) $(CFLAGS) -Fo"$@" "$<"


{$(MATLAB_ROOT)\simulink\src}.cpp.obj :
	$(CPP) $(CPPFLAGS) -Fo"$@" "$<"


{$(MATLAB_ROOT)\toolbox\coder\xcp\src\target\slave\protocol\src}.c.obj :
	$(CC) $(CFLAGS) -Fo"$@" "$<"


{$(MATLAB_ROOT)\toolbox\coder\xcp\src\target\slave\protocol\src}.cpp.obj :
	$(CPP) $(CPPFLAGS) -Fo"$@" "$<"


{$(MATLAB_ROOT)\toolbox\coder\xcp\src\target\slave\transport\src}.c.obj :
	$(CC) $(CFLAGS) -Fo"$@" "$<"


{$(MATLAB_ROOT)\toolbox\coder\xcp\src\target\slave\transport\src}.cpp.obj :
	$(CPP) $(CPPFLAGS) -Fo"$@" "$<"


{$(MATLAB_ROOT)\toolbox\coder\xcp\src\target\ext_mode\src}.c.obj :
	$(CC) $(CFLAGS) -Fo"$@" "$<"


{$(MATLAB_ROOT)\toolbox\coder\xcp\src\target\ext_mode\src}.cpp.obj :
	$(CPP) $(CPPFLAGS) -Fo"$@" "$<"


{$(MATLAB_ROOT)\toolbox\coder\xcp\src\target\slave\platform\default}.c.obj :
	$(CC) $(CFLAGS) -Fo"$@" "$<"


{$(MATLAB_ROOT)\toolbox\coder\xcp\src\target\slave\platform\default}.cpp.obj :
	$(CPP) $(CPPFLAGS) -Fo"$@" "$<"


{$(MATLAB_ROOT)\toolbox\coder\rtiostream\src\rtiostreamtcpip}.c.obj :
	$(CC) $(CFLAGS) -Fo"$@" "$<"


{$(MATLAB_ROOT)\toolbox\coder\rtiostream\src\rtiostreamtcpip}.cpp.obj :
	$(CPP) $(CPPFLAGS) -Fo"$@" "$<"


rtwdemo_secondOrderSystem.obj : $(START_DIR)\rtwdemo_secondOrderSystem_grt_rtw\rtwdemo_secondOrderSystem.c
	$(CC) $(CFLAGS) -Fo"$@" $(START_DIR)\rtwdemo_secondOrderSystem_grt_rtw\rtwdemo_secondOrderSystem.c


rtwdemo_secondOrderSystem_data.obj : $(START_DIR)\rtwdemo_secondOrderSystem_grt_rtw\rtwdemo_secondOrderSystem_data.c
	$(CC) $(CFLAGS) -Fo"$@" $(START_DIR)\rtwdemo_secondOrderSystem_grt_rtw\rtwdemo_secondOrderSystem_data.c


rt_main.obj : $(MATLAB_ROOT)\rtw\c\src\common\rt_main.c
	$(CC) $(CFLAGS) -Fo"$@" $(MATLAB_ROOT)\rtw\c\src\common\rt_main.c


xcp_ext_common.obj : $(MATLAB_ROOT)\toolbox\coder\xcp\src\target\ext_mode\src\xcp_ext_common.c
	$(CC) $(CFLAGS) -Fo"$@" $(MATLAB_ROOT)\toolbox\coder\xcp\src\target\ext_mode\src\xcp_ext_common.c


xcp_ext_classic_trigger.obj : $(MATLAB_ROOT)\toolbox\coder\xcp\src\target\ext_mode\src\xcp_ext_classic_trigger.c
	$(CC) $(CFLAGS) -Fo"$@" $(MATLAB_ROOT)\toolbox\coder\xcp\src\target\ext_mode\src\xcp_ext_classic_trigger.c


xcp.obj : $(MATLAB_ROOT)\toolbox\coder\xcp\src\target\slave\protocol\src\xcp.c
	$(CC) $(CFLAGS) -Fo"$@" $(MATLAB_ROOT)\toolbox\coder\xcp\src\target\slave\protocol\src\xcp.c


xcp_standard.obj : $(MATLAB_ROOT)\toolbox\coder\xcp\src\target\slave\protocol\src\xcp_standard.c
	$(CC) $(CFLAGS) -Fo"$@" $(MATLAB_ROOT)\toolbox\coder\xcp\src\target\slave\protocol\src\xcp_standard.c


xcp_daq.obj : $(MATLAB_ROOT)\toolbox\coder\xcp\src\target\slave\protocol\src\xcp_daq.c
	$(CC) $(CFLAGS) -Fo"$@" $(MATLAB_ROOT)\toolbox\coder\xcp\src\target\slave\protocol\src\xcp_daq.c


xcp_calibration.obj : $(MATLAB_ROOT)\toolbox\coder\xcp\src\target\slave\protocol\src\xcp_calibration.c
	$(CC) $(CFLAGS) -Fo"$@" $(MATLAB_ROOT)\toolbox\coder\xcp\src\target\slave\protocol\src\xcp_calibration.c


xcp_fifo.obj : $(MATLAB_ROOT)\toolbox\coder\xcp\src\target\slave\transport\src\xcp_fifo.c
	$(CC) $(CFLAGS) -Fo"$@" $(MATLAB_ROOT)\toolbox\coder\xcp\src\target\slave\transport\src\xcp_fifo.c


xcp_transport.obj : $(MATLAB_ROOT)\toolbox\coder\xcp\src\target\slave\transport\src\xcp_transport.c
	$(CC) $(CFLAGS) -Fo"$@" $(MATLAB_ROOT)\toolbox\coder\xcp\src\target\slave\transport\src\xcp_transport.c


xcp_mem_default.obj : $(MATLAB_ROOT)\toolbox\coder\xcp\src\target\slave\platform\default\xcp_mem_default.c
	$(CC) $(CFLAGS) -Fo"$@" $(MATLAB_ROOT)\toolbox\coder\xcp\src\target\slave\platform\default\xcp_mem_default.c


xcp_drv_rtiostream.obj : $(MATLAB_ROOT)\toolbox\coder\xcp\src\target\slave\platform\default\xcp_drv_rtiostream.c
	$(CC) $(CFLAGS) -Fo"$@" $(MATLAB_ROOT)\toolbox\coder\xcp\src\target\slave\platform\default\xcp_drv_rtiostream.c


xcp_frame_tcp.obj : $(MATLAB_ROOT)\toolbox\coder\xcp\src\target\slave\transport\src\xcp_frame_tcp.c
	$(CC) $(CFLAGS) -Fo"$@" $(MATLAB_ROOT)\toolbox\coder\xcp\src\target\slave\transport\src\xcp_frame_tcp.c


xcp_ext_param_default_tcp.obj : $(MATLAB_ROOT)\toolbox\coder\xcp\src\target\ext_mode\src\xcp_ext_param_default_tcp.c
	$(CC) $(CFLAGS) -Fo"$@" $(MATLAB_ROOT)\toolbox\coder\xcp\src\target\ext_mode\src\xcp_ext_param_default_tcp.c


xcp_platform_default.obj : $(MATLAB_ROOT)\toolbox\coder\xcp\src\target\slave\platform\default\xcp_platform_default.c
	$(CC) $(CFLAGS) -Fo"$@" $(MATLAB_ROOT)\toolbox\coder\xcp\src\target\slave\platform\default\xcp_platform_default.c


rtiostream_tcpip.obj : $(MATLAB_ROOT)\toolbox\coder\rtiostream\src\rtiostreamtcpip\rtiostream_tcpip.c
	$(CC) $(CFLAGS) -Fo"$@" $(MATLAB_ROOT)\toolbox\coder\rtiostream\src\rtiostreamtcpip\rtiostream_tcpip.c


###########################################################################
## DEPENDENCIES
###########################################################################

$(ALL_OBJS) : rtw_proj.tmw $(COMPILER_COMMAND_FILE) $(MAKEFILE)


###########################################################################
## MISCELLANEOUS TARGETS
###########################################################################

info : 
	@cmd /C "@echo ### PRODUCT = $(PRODUCT)"
	@cmd /C "@echo ### PRODUCT_TYPE = $(PRODUCT_TYPE)"
	@cmd /C "@echo ### BUILD_TYPE = $(BUILD_TYPE)"
	@cmd /C "@echo ### INCLUDES = $(INCLUDES)"
	@cmd /C "@echo ### DEFINES = $(DEFINES)"
	@cmd /C "@echo ### ALL_SRCS = $(ALL_SRCS)"
	@cmd /C "@echo ### ALL_OBJS = $(ALL_OBJS)"
	@cmd /C "@echo ### LIBS = $(LIBS)"
	@cmd /C "@echo ### MODELREF_LIBS = $(MODELREF_LIBS)"
	@cmd /C "@echo ### SYSTEM_LIBS = $(SYSTEM_LIBS)"
	@cmd /C "@echo ### TOOLCHAIN_LIBS = $(TOOLCHAIN_LIBS)"
	@cmd /C "@echo ### CFLAGS = $(CFLAGS)"
	@cmd /C "@echo ### LDFLAGS = $(LDFLAGS)"
	@cmd /C "@echo ### SHAREDLIB_LDFLAGS = $(SHAREDLIB_LDFLAGS)"
	@cmd /C "@echo ### CPPFLAGS = $(CPPFLAGS)"
	@cmd /C "@echo ### CPP_LDFLAGS = $(CPP_LDFLAGS)"
	@cmd /C "@echo ### CPP_SHAREDLIB_LDFLAGS = $(CPP_SHAREDLIB_LDFLAGS)"
	@cmd /C "@echo ### ARFLAGS = $(ARFLAGS)"
	@cmd /C "@echo ### MEX_CFLAGS = $(MEX_CFLAGS)"
	@cmd /C "@echo ### MEX_CPPFLAGS = $(MEX_CPPFLAGS)"
	@cmd /C "@echo ### MEX_LDFLAGS = $(MEX_LDFLAGS)"
	@cmd /C "@echo ### MEX_CPPLDFLAGS = $(MEX_CPPLDFLAGS)"
	@cmd /C "@echo ### DOWNLOAD_FLAGS = $(DOWNLOAD_FLAGS)"
	@cmd /C "@echo ### EXECUTE_FLAGS = $(EXECUTE_FLAGS)"
	@cmd /C "@echo ### MAKE_FLAGS = $(MAKE_FLAGS)"


clean : 
	$(ECHO) "### Deleting all derived files..."
	@if exist $(PRODUCT) $(RM) $(PRODUCT)
	$(RM) $(ALL_OBJS)
	$(ECHO) "### Deleted all derived files."



% Pfosten_.nc
N2 (------------------------ General Infos -------------------------)
N4 (LIGNOCAM_VERSION=19.1.2)
N6 (USERPROFIL=C:\ProgramData\lignocam\UserProfil\twmillE_Balteschwiler_M)
N8 (XAM_GUID={1B18AD9F-DCA1-4475-A3E5-390E9605D58E})
N10 (XAM_DATE=)
N12 (XAM_FILENAME=Hackathon.XAM)
N14 (LOAD_UID=2)
N16 (LOAD_NAME=Pfosten_)
N18 (LOAD_COMMENT=Bemerkung Charge: .......)
N20 (ISOCODE_DATE=09.02.25 20:05:52)
N22 (ISOCODE_FILENAME=Pfosten_.nc)
N24 (---------------------- End General Infos -----------------------)
N26 (PNr 3, X = 2500.0, Y = 140.0, Z = 140.0)
N28 L steuer_TW.up
N30 V.P.CHARGENLAENGE = 2500.0
N32 V.P.CHARGENBREITE = 140.0
N34 V.P.CHARGENHOEHE = 140.0
N36 V.P.Z_Sicherheitsdistanz=40.00
N38 G54 G161
N40 V.P.LINE_RASTERTABLE     = 4
N42 V.P.ROW_RASTERTABLE      = 210
N44 V.P.QUADRANT_RASTERTABLE = 0
N46 V.P.ROW_DISTANCE         = 250.0
N48 V.P.LINE_DISTANCE        = 250.0
N50 V.P.BOLT_DIAMETER        =  50.0
N52 V.P.CHARGE_X_OFFSET = 0.0
N54 V.P.CHARGE_Y_OFFSET = 0.0
N56 V.P.CHARGE_Z_OFFSET = 0.0
N58 (LC_CHARGEN_NR=2 LC_MACRO_INDEX_START=4  LC_MACRO_INDEX_END=6)
N60 (PART    1  52525  55025   2500 CLAMPING_NR 1 Pro-Nr 3)
N62 (KKR X=52525.0 Y=-3624.5 Z= -162.0)
N64 (KKD X= 2500.0 Y=  140.0 Z=  140.0)
N66 (T=202   P=0    TD=0    D=997.0    L=7.0)
N68 (T=62   P=0    TD=0    D=16.0     L=488.0)
N70 (LC_MOVE_SPINDLE_1_TO_PARK Y_PARK -5580.0  Z_PARK 1080.0   A_PARK 90.0   C_PARK 90.0   )
N72 (LC_MOVE_SPINDLE_2_TO_PARK X_PARK 52525.0  Y_PARK 740.0    Z_PARK 1000.0   A_PARK 90.0   C_PARK 180.0  )
N74 #VAR
N76 V.P.T_NR[60] = [202, 62, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
N78 #ENDVAR
N80 L TOOLNR_Check.up
N82 #VAR
N84 V.P.FEEDPAR[20] = [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
N86 #ENDVAR
N88 L COLL.up
N90 L feed.up
N92 #VAR
N94 V.P.PRE_SEL_TOOL_NR[6] = [62, 0, 0, 0, 0, 0]
N96 #ENDVAR
N98 L PRE_SEL_TOOL.UP
N100 T202 LM06
N102 (LC_OPEN_DOOR)
N104 L PRE_D
N106 D202
N108 L PAST_D
N110 #RTCP ON
N112 M3 S750
N114 #MCS ON
N116 G90 G40 G00 Y     0.00 Z  1000.00 A    90.00 C   180.00 
N118 G90 G40 G00 A    90.00 C   -90.00 
N120 #MCS OFF
N122 G90 G40 G00 A    90.00 C   -90.00 
N124 M3 S1400
N126 G90 G40 G00 X 52525.00 Y   915.00 
N128 G90 G40 G00 Z   678.50 
N130 (-------MK1006 ML6 1 KF 2-10-2 3 Abschnitt bei +Z, von -------)
N132 (ACTIVE_MODEL_LIST=1)
N134 #VAR
N136 V.P.Macro[4] = [1006, 2, 10, 1]
N138 #ENDVAR
N140 L Macro_Start.up
N142 L Spindle_OK.up
N144 #CS DEF [5] [ 52525.00,    775.00,      0.00,    -90.00,      0.00,     90.00]
N146 #CS ON [5]
N148 V.P.CS_X = 52525.0 V.P.CS_Y = 775.0 V.P.CS_Z = 0.0 V.P.CS_X_Angle = -90.0 V.P.CS_Y_Angle = 0.0 V.P.CS_Z_Angle = 90.0
N150 G40 G00 X140.000    Y-678.500   Z0.000     
N152 G41 G01 X140.000    Y0.600      Z0.000      F3000
N154 G41 G01 X-0.000     Y0.600      Z0.000      F6000
N156 G40 G01 X-0.000     Y-678.500   Z0.000      F40500
N158 #CS OFF
N160 L Macro_End.up
N162 (END_OF_MACRO)
N164 M3 S750
N166 #RTCP OFF
N168 D0
N170 G90 G40 G00 Z   960.82 
N172 M3 S750
N174 L Spindle_OK.up
N176 G90 G40 G00 A    90.00 C    90.00 
N178 L PRE_D
N180 D202
N182 L PAST_D
N184 #RTCP ON
N186 G90 G40 G00 A    90.00 C    90.00 
N188 M3 S1400
N190 G90 G40 G00 X 55025.00 Y   775.00 
N192 G90 G40 G00 Z   678.50 
N194 (-------MK1006 ML5 2 KF 1-10-2 2 Abschnitt bei +Z, von -------)
N196 (ACTIVE_MODEL_LIST=1)
N198 #VAR
N200 V.P.Macro[4] = [1006, 1, 10, 2]
N202 #ENDVAR
N204 L Macro_Start.up
N206 L Spindle_OK.up
N208 #CS DEF [5] [ 55025.00,    775.00,      0.00,     90.00,      0.00,     90.00]
N210 #CS ON [5]
N212 V.P.CS_X = 55025.0 V.P.CS_Y = 775.0 V.P.CS_Z = 0.0 V.P.CS_X_Angle = 90.0 V.P.CS_Y_Angle = 0.0 V.P.CS_Z_Angle = 90.0
N214 G40 G00 X-0.000     Y678.500    Z0.000     
N216 G41 G01 X-0.000     Y-0.600     Z0.000      F3000
N218 G41 G01 X140.000    Y-0.600     Z0.000      F6000
N220 G40 G01 X140.000    Y678.500    Z0.000      F40500
N222 #CS OFF
N224 L Macro_End.up
N226 (END_OF_MACRO)
N228 M3 S750
N230 L Spindle_OK.up
N232 M05 
N234 #MCS ON
N236 G90 G40 G00 Y     0.00 Z  1000.00 C   180.00 
N238 G90 G40 G00 A    90.00 C   180.00 
N240 #MCS OFF
N242 #RTCP OFF
N244 #VAR
N246 V.P.PRE_SEL_TOOL_NR[6] = [0, 0, 0, 0, 0, 0]
N248 #ENDVAR
N250 L PRE_SEL_TOOL.UP
N252 (LC_MOVE_SPINDLE_2_TO_PARK Y_PARK 740.0    Z_PARK 1000.0   A_PARK 90.0   C_PARK 180.0  )
N254 T62 LM06
N256 (LC_CLOSE_DOOR)
N258 L PRE_D
N260 D62
N262 L PAST_D
N264 #RTCP ON
N266 M3 S1200
N268 #MCS ON
N270 G90 G40 G00 Y -4500.00 Z  1080.00 A     0.00 C     0.00 
N272 G90 G40 G00 A    90.00 C    90.00 
N274 #MCS OFF
N276 G90 G40 G00 A    90.00 C    90.00 
N278 G90 G40 G00 X 55065.00 Y   845.00 
N280 G90 G40 G00 Z    70.00 
N282 (-------MK1401 ML4 2 KF 4-40-6 1 Bohrung Bohrer-------)
N284 (ACTIVE_MODEL_LIST=1)
N286 #VAR
N288 V.P.Macro[4] = [1401, 4, 40, 2]
N290 #ENDVAR
N292 L Macro_Start.up
N294 L Spindle_OK.up
N296 #CS DEF [5] [ 55025.00,    845.00,     70.00,      0.00,     90.00,      0.00]
N298 #CS ON [5]
N300 V.P.CS_X = 55025.0 V.P.CS_Y = 845.0 V.P.CS_Z = 70.0 V.P.CS_X_Angle = 0.0 V.P.CS_Y_Angle = 90.0 V.P.CS_Z_Angle = 0.0
N302 G40 G00 X0.000      Y0.000      Z40.000    
N304 G40 G01 X-0.000     Y0.000      Z-134.700   F3000
N306 G40 G01 X0.000      Y0.000      Z40.000     F22500
N308 #CS OFF
N310 L Macro_End.up
N312 (END_OF_MACRO)
N314 M5
N316 #MCS ON
N318 G90 G40 G00 Z  1080.00 
N320 G90 G40 G00 Y -4500.00 Z  1080.00 C     0.00 
N322 G90 G40 G00 A     0.00 C     0.00 
N324 #MCS OFF
N326 #RTCP OFF
N328 G162
N330 #DELETE V.P.FEEDPAR
N332 #VAR
N334 V.P.FEEDPAR[20] = [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
N336 #ENDVAR
N338 L feed.up (AUSFOERDERN)
N340 M30
N342 (LC_INTERRUPT_CLASH_DETECTION)
N344 (LC_INTERRUPT_SIMULATION)
N346 #COMMENT BEGIN
N348 	[GENERAL]
N350 		PROJECTNUMBER: ""
N352 		PROJECTNAME: ""
N354 		CUSTOMER: ""
N356 	[ENDGENERAL]
N358 	[PART]
N360 		COUNT: "1"
N362 		SINGLEMEMBERNUMBER: "3"
N364 		LENGTH: "2500.0"
N366 		WIDTH: "140.0"
N368 		HEIGHT: "140.0"
N370 		GROUP: ""
N372 		STOREY: "Geschoss 1"
N374 		MATERIAL: "Sapin"
N376 		USERATTRIBUTE 1: ""LC_PART_SHADE_AREA": "0.35""
N378 		USERATTRIBUTE 2: ""LC_NET_VOLUME": "0.05""
N380 		USERATTRIBUTE 3: ""LC_ROHLING_VOLUME": "0.05""
N382 	[ENDPART]
N384 	[LIGNOCAM]
N386 		XAMGUID: "{1B18AD9F-DCA1-4475-A3E5-390E9605D58E}"
N388 		LOADUID: "2"
N390 	[ENDLIGNOCAM]
N392 	[UID2BPRODUCED]
N394 		SINGLEMEMBERNUMBER: "3"
N396 		DESIGNATION: "Pfosten"
N398 		GROUP: ""
N400 		STOREYTYPE: "CEILING"
N402 		PARTTYPE: "PART"
N404 		COMPOSITETYPE: ""
N406 		COUNTPARTLOAD: "1"
N408 		COUNT2BPRODUCED: "1"
N410 		UID: "2"
N412 		GUID: "{33555AD1-0326-4DA5-A2BF-7106EBA243D4}"
N414 	[ENDUID2BPRODUCED]
N416 #COMMENT END
N418 (LC_CONTINUE_CLASH_DETECTION)
N420 (LC_CONTINUE_SIMULATION)

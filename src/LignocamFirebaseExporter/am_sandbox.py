# Step 1: Install required libraries
# Run this command in your terminal
# pip install firebase-admin
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger()

import firebase_admin
from firebase_admin import firestore, credentials

from CONFIG import *

# Step 2: Initialize Firebase Admin SDK
cred = credentials.Certificate("./projects-talking-firebase-config.json")
firebase_admin.initialize_app(cred)

# Step 3: Connect to Firestore
db = firestore.client()

def create_project(guid, attrs: dict = None):
  doc_ref = db.collection(PROJECTS).document()
  id = doc_ref.id
  project_data = {
    u'guid': guid,
    u'id': id
  }
  if attrs:
    project_data.update(attrs)
  doc_ref.set(project_data)
  return find_project_by_guid(guid)[0]

def get_or_create_project(guid):
  projects = find_project_by_guid(guid)
  if projects:
    log.info(f'Found project with guid: {guid}')
    return projects[0]
  else:
    log.info(f'Creating project with guid: {guid}')
    create_project(guid)
    return find_project_by_guid(guid)[0]

def create_part(guid, attrs: dict = None):
  doc_ref = db.collection(PARTS).document()
  id = doc_ref.id
  part_data = {
      u'guid': guid,
      u'id': id
  }
  if attrs:
    part_data.update(attrs)
  doc_ref.set(part_data)
  return find_part_by_guid(guid)[0]

def find_project_by_name(name):
  projects = db.collection(PROJECTS).where(u'name', u'==', name).stream()
  return [project for project in projects]

def find_project_by_guid(guid):
  projects = db.collection(PROJECTS).where(u'guid', u'==', guid).stream()
  return [project for project in projects]

def find_part_by_guid(guid):
  parts = db.collection(PARTS).where(u'guid', u'==', guid).stream()
  return [part for part in parts]

def delete_prject_by_guid(guid):
  projects = find_project_by_guid(guid)
  for project in projects:
    project.reference.delete()

def delete_part_by_guid(guid):
  parts = db.collection(PARTS).where(u'guid', u'==', guid).stream()
  for part in parts:
    part.reference.delete()

def fetch_all_projects():
  projects = db.collection(PROJECTS).stream()
  return [project for project in projects]

def delete_all_projects():
  projects = db.collection(PROJECTS).stream()
  for project in projects:
    project.reference.delete()

def get_project_name(id):
  project = db.collection(PROJECTS).document(id).get()
  return project.to_dict()['name']

def set_project_name(project_id, name):
  log.info(f'Setting name for project: {project_id}')
  project_ref = db.collection(PROJECTS).document(project_id)
  project_ref.update({
    u'name': name
  })

def add_cam_data(project_id, cam_data):
  log.info(f'Adding cam data to project: {project_id}')
  project_ref = db.collection(PROJECTS).document(project_id)
  project_ref.update({
    u'cam_data': cam_data
  })

def set_project_guid(project_id, guid):
  log.info(f'Setting guid for project: {project_id}')
  project_ref = db.collection(PROJECTS).document(project_id)
  project_ref.update({
    u'guid': guid
  })

# Use this function to (re-)generate test data
def generate_test_data():
  delete_prject_by_guid(TEST_PROJECT_GUID)
  project = create_project(TEST_PROJECT_GUID, {u'name': TEST_PROJECT_NAME})
  project_data = project.to_dict()
  delete_part_by_guid(TEST_PROJECT_PART_GUIDS[0])
  create_part(TEST_PROJECT_PART_GUIDS[0], {
    u'project_guid': project_data['guid'],
    u'cam_data': {
      u'production_time_simulated': 228358,
      u'loadUID': 1,
      u'reverse':'A',
      u'iso_code': r"""% Pfette_.nc
N2 (------------------------ General Infos -------------------------)
N4 (LIGNOCAM_VERSION=19.1.2)
N6 (USERPROFIL=C:\ProgramData\lignocam\UserProfil\twmillE_Balteschwiler_M)
N8 (XAM_GUID={DC96C21E-8755-412F-8FAA-B64E5DADBA6A})
N10 (XAM_DATE=08.02.2025 19:01:56)
N12 (XAM_FILENAME=Hackathon.xam)
N14 (LOAD_UID=1)
N16 (LOAD_NAME=Pfette_)
N18 (LOAD_COMMENT=Bemerkung Charge: .......)
N20 (ISOCODE_DATE=08.02.25 20:10:42)
N22 (ISOCODE_FILENAME=Pfette_.nc)
N24 (---------------------- End General Infos -----------------------)
N26 (PNr 2, X = 2000.0, Y = 200.0, Z = 140.0)
N28 L steuer_TW.up
N30 V.P.CHARGENLAENGE = 2000.0
N32 V.P.CHARGENBREITE = 200.0
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
N58 (LC_CHARGEN_NR=1 LC_MACRO_INDEX_START=7  LC_MACRO_INDEX_END=10)
N60 (PART    1  52525  54525   2000 CLAMPING_NR 1 Pro-Nr 2)
N62 (KKR X=52525.0 Y=-3624.5 Z= -162.0)
N64 (KKD X= 2000.0 Y=  200.0 Z=  140.0)
N66 (T=202   P=0    TD=0    D=997.0    L=7.0)
N68 (T=152   P=0    TD=0    D=30.0     L=227.6)
N70 (T=62   P=0    TD=0    D=16.0     L=488.0)
N72 (LC_MOVE_SPINDLE_1_TO_PARK Y_PARK -5580.0  Z_PARK 1080.0   A_PARK 90.0   C_PARK 90.0   )
N74 (LC_MOVE_SPINDLE_2_TO_PARK X_PARK 52525.0  Y_PARK 740.0    Z_PARK 1000.0   A_PARK 90.0   C_PARK 180.0  )
N76 #VAR
N78 V.P.T_NR[60] = [202, 152, 62, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
N80 #ENDVAR
N82 L TOOLNR_Check.up
N84 #VAR
N86 V.P.FEEDPAR[20] = [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
N88 #ENDVAR
N90 L COLL.up
N92 L feed.up
N94 #VAR
N96 V.P.PRE_SEL_TOOL_NR[6] = [152, 62, 0, 0, 0, 0]
N98 #ENDVAR
N100 L PRE_SEL_TOOL.UP
N102 T202 LM06
N104 (LC_OPEN_DOOR)
N106 L PRE_D
N108 D202
N110 L PAST_D
N112 #RTCP ON
N114 M3 S750
N116 #MCS ON
N118 G90 G40 G00 Y     0.00 Z  1000.00 A    90.00 C   180.00 
N120 G90 G40 G00 A    90.00 C   -90.00 
N122 #MCS OFF
N124 G90 G40 G00 A    90.00 C   -90.00 
N126 M3 S1400
N128 G90 G40 G00 X 52525.00 Y   975.00 
N130 G90 G40 G00 Z   678.50 
N132 (-------MK1006 ML9 1 KF 2-10-2 3 Abschnitt bei +Z, von -------)
N134 (ACTIVE_MODEL_LIST=1)
N136 #VAR
N138 V.P.Macro[4] = [1006, 2, 10, 1]
N140 #ENDVAR
N142 L Macro_Start.up
N144 L Spindle_OK.up
N146 #CS DEF [5] [ 52525.00,    775.00,      0.00,    -90.00,      0.00,     90.00]
N148 #CS ON [5]
N150 V.P.CS_X = 52525.0 V.P.CS_Y = 775.0 V.P.CS_Z = 0.0 V.P.CS_X_Angle = -90.0 V.P.CS_Y_Angle = 0.0 V.P.CS_Z_Angle = 90.0
N152 G40 G00 X200.000    Y-678.500   Z0.000     
N154 G41 G01 X200.000    Y0.600      Z0.000      F3000
N156 G41 G01 X-0.000     Y0.600      Z0.000      F6000
N158 G40 G01 X0.000      Y-678.500   Z0.000      F40500
N160 #CS OFF
N162 L Macro_End.up
N164 (END_OF_MACRO)
N166 M3 S750
N168 #RTCP OFF
N170 D0
N172 G90 G40 G00 Z   960.82 
N174 M3 S750
N176 L Spindle_OK.up
N178 G90 G40 G00 A    90.00 C    90.00 
N180 L PRE_D
N182 D202
N184 L PAST_D
N186 #RTCP ON
N188 G90 G40 G00 A    90.00 C    90.00 
N190 M3 S1400
N192 G90 G40 G00 X 54525.00 Y   775.00 
N194 G90 G40 G00 Z   678.50 
N196 (-------MK1006 ML8 2 KF 1-10-2 2 Abschnitt bei +Z, von -------)
N198 (ACTIVE_MODEL_LIST=1)
N200 #VAR
N202 V.P.Macro[4] = [1006, 1, 10, 2]
N204 #ENDVAR
N206 L Macro_Start.up
N208 L Spindle_OK.up
N210 #CS DEF [5] [ 54525.00,    775.00,      0.00,     90.00,      0.00,     90.00]
N212 #CS ON [5]
N214 V.P.CS_X = 54525.0 V.P.CS_Y = 775.0 V.P.CS_Z = 0.0 V.P.CS_X_Angle = 90.0 V.P.CS_Y_Angle = 0.0 V.P.CS_Z_Angle = 90.0
N216 G40 G00 X0.000      Y678.500    Z0.000     
N218 G41 G01 X0.000      Y-0.600     Z0.000      F3000
N220 G41 G01 X200.000    Y-0.600     Z0.000      F6000
N222 G40 G01 X200.000    Y678.500    Z0.000      F40500
N224 #CS OFF
N226 L Macro_End.up
N228 (END_OF_MACRO)
N230 M3 S750
N232 L Spindle_OK.up
N234 M05 
N236 #MCS ON
N238 G90 G40 G00 Y     0.00 Z  1000.00 C   180.00 
N240 G90 G40 G00 A    90.00 C   180.00 
N242 #MCS OFF
N244 #RTCP OFF
N246 #VAR
N248 V.P.PRE_SEL_TOOL_NR[6] = [62, 0, 0, 0, 0, 0]
N250 #ENDVAR
N252 L PRE_SEL_TOOL.UP
N254 (LC_MOVE_SPINDLE_2_TO_PARK Y_PARK 740.0    Z_PARK 1000.0   A_PARK 90.0   C_PARK 180.0  )
N256 T152 LM06
N258 (LC_CLOSE_DOOR)
N260 L PRE_D
N262 D152
N264 L PAST_D
N266 #RTCP ON
N268 M3 S12000
N270 #MCS ON
N272 G90 G40 G00 Y -4500.00 Z  1080.00 A     0.00 C     0.00 
N274 G90 G40 G00 A    90.00 C     0.00 
N276 #MCS OFF
N278 G90 G40 G00 A    90.00 C     0.00 
N280 G90 G40 G00 X 52650.00 Y   735.00 
N282 G90 G40 G00 Z   160.00 
N284 (-------MK1351 ML10 6 KF 4-30-1 4 Blatt, Schruppen und S-------)
N286 (ACTIVE_MODEL_LIST=1)
N288 #VAR
N290 V.P.Macro[4] = [1351, 4, 30, 6]
N292 #ENDVAR
N294 L Macro_Start.up
N296 L Spindle_OK.up
N298 #CS DEF [5] [ 52665.00,    805.00,    140.00,    -90.00,      0.00,    180.00]
N300 #CS ON [5]
N302 V.P.CS_X = 52665.0 V.P.CS_Y = 805.0 V.P.CS_Z = 140.0 V.P.CS_X_Angle = -90.0 V.P.CS_Y_Angle = 0.0 V.P.CS_Z_Angle = 180.0
N304 G40 G01 X15.000     Y-20.000    Z70.000     F45000
N306 G40 G01 X15.000     Y-20.000    Z0.000      F8000
N308 G40 G01 X15.000     Y15.000     Z0.000      F4000
N310 G40 G01 X15.000     Y15.000     Z70.000     F40500
N312 G40 G01 X15.000     Y160.000    Z70.000     F40500
N314 G40 G01 X15.000     Y160.000    Z0.000      F8000
N316 G40 G01 X15.000     Y125.000    Z0.000      F4000
N318 G40 G01 X15.100     Y140.000    Z0.000      F8000
N320 G40 G01 X140.000    Y140.000    Z0.000      F8000
N322 G40 G01 X140.000    Y0.000      Z0.000      F8000
N324 G40 G01 X15.100     Y0.000      Z0.000      F8000
N326 G40 G01 X15.100     Y0.000      Z70.000     F40500
N328 G40 G01 X16.000     Y-20.000    Z70.000     F45000
N330 G40 G01 X16.000     Y-20.000    Z0.000      F8000
N332 G40 G01 X16.000     Y13.400     Z0.000      F4000
N334 G40 G01 X140.000    Y13.400     Z0.000      F8000
N336 G40 G01 X140.000    Y41.800     Z0.000      F8000
N338 G40 G01 X16.000     Y41.800     Z0.000      F8000
N340 G40 G01 X16.000     Y70.200     Z0.000      F8000
N342 G40 G01 X140.000    Y70.200     Z0.000      F8000
N344 G40 G01 X140.000    Y98.600     Z0.000      F8000
N346 G40 G01 X16.000     Y98.600     Z0.000      F8000
N348 G40 G01 X16.000     Y127.000    Z0.000      F8000
N350 G40 G01 X140.000    Y127.000    Z0.000      F8000
N352 G40 G01 X140.000    Y127.000    Z70.000     F40500
N354 G40 G01 X16.000     Y-20.000    Z70.000     F45000
N356 G40 G01 X16.000     Y-20.000    Z0.000      F8000
N358 G42 G01 X0.000      Y0.000      Z0.000      F4000
N360 G42 G01 X0.000      Y140.000    Z0.000      F8000
N362 G40 G01 X15.200     Y140.000    Z0.000      F8000
N364 G40 G01 X15.200     Y140.000    Z70.000     F40500
N366 G40 G01 X15.200     Y140.000    Z70.000     F40500
N368 #CS OFF
N370 L Macro_End.up
N372 (END_OF_MACRO)
N374 M3 S12000
N376 L Spindle_OK.up
N378 M05 
N380 #MCS ON
N382 G90 G40 G00 Z  1080.00 
N384 G90 G40 G00 Y -4500.00 Z  1080.00 C     0.00 
N386 G90 G40 G00 A     0.00 C     0.00 
N388 #MCS OFF
N390 #RTCP OFF
N392 #VAR
N394 V.P.PRE_SEL_TOOL_NR[6] = [0, 0, 0, 0, 0, 0]
N396 #ENDVAR
N398 L PRE_SEL_TOOL.UP
N400 T62 LM06
N402 (LC_CLOSE_DOOR)
N404 L PRE_D
N406 D62
N408 L PAST_D
N410 #RTCP ON
N412 M3 S1200
N414 #MCS ON
N416 G90 G40 G00 Y -4500.00 Z  1080.00 A     0.00 C     0.00 
N418 G90 G40 G00 A    90.00 C   180.00 
N420 #MCS OFF
N422 G90 G40 G00 A    90.00 C   180.00 
N424 G90 G40 G00 X 52595.00 Y  1015.00 
N426 G90 G40 G00 Z    70.00 
N428 (-------MK1401 ML7 4 KF 4-40-3 1 Bohrung Bohrer-------)
N430 (ACTIVE_MODEL_LIST=1)
N432 #VAR
N434 V.P.Macro[4] = [1401, 4, 40, 4]
N436 #ENDVAR
N438 L Macro_Start.up
N440 L Spindle_OK.up
N442 #CS DEF [5] [ 52595.00,    975.00,     70.00,      0.00,     90.00,     90.00]
N444 #CS ON [5]
N446 V.P.CS_X = 52595.0 V.P.CS_Y = 975.0 V.P.CS_Z = 70.0 V.P.CS_X_Angle = 0.0 V.P.CS_Y_Angle = 90.0 V.P.CS_Z_Angle = 90.0
N448 G40 G00 X0.000      Y0.000      Z40.000    
N450 G40 G01 X-0.000     Y-0.000     Z-175.000   F3000
N452 G40 G01 X0.000      Y0.000      Z40.000     F22500
N454 #CS OFF
N456 L Macro_End.up
N458 (END_OF_MACRO)
N460 M5
N462 #MCS ON
N464 G90 G40 G00 Z  1080.00 
N466 G90 G40 G00 Y -4500.00 Z  1080.00 C     0.00 
N468 G90 G40 G00 A     0.00 C     0.00 
N470 #MCS OFF
N472 #RTCP OFF
N474 G162
N476 #DELETE V.P.FEEDPAR
N478 #VAR
N480 V.P.FEEDPAR[20] = [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
N482 #ENDVAR
N484 L feed.up (AUSFOERDERN)
N486 M30
N488 (LC_INTERRUPT_CLASH_DETECTION)
N490 (LC_INTERRUPT_SIMULATION)
N492 #COMMENT BEGIN
N494 	[GENERAL]
N496 		PROJECTNUMBER: ""
N498 		PROJECTNAME: ""
N500 		CUSTOMER: ""
N502 	[ENDGENERAL]
N504 	[PART]
N506 		COUNT: "1"
N508 		SINGLEMEMBERNUMBER: "2"
N510 		LENGTH: "2000.0"
N512 		WIDTH: "140.0"
N514 		HEIGHT: "200.0"
N516 		GROUP: ""
N518 		STOREY: "Geschoss 1"
N520 		MATERIAL: "Sapin"
N522 		USERATTRIBUTE 1: ""LC_PART_SHADE_AREA": "0.40""
N524 		USERATTRIBUTE 2: ""LC_NET_VOLUME": "0.06""
N526 		USERATTRIBUTE 3: ""LC_ROHLING_VOLUME": "0.06""
N528 	[ENDPART]
N530 	[LIGNOCAM]
N532 		XAMGUID: "{DC96C21E-8755-412F-8FAA-B64E5DADBA6A}"
N534 		LOADUID: "1"
N536 	[ENDLIGNOCAM]
N538 	[UID2BPRODUCED]
N540 		SINGLEMEMBERNUMBER: "2"
N542 		DESIGNATION: "Pfette"
N544 		GROUP: ""
N546 		STOREYTYPE: "CEILING"
N548 		PARTTYPE: "PART"
N550 		COMPOSITETYPE: ""
N552 		COUNTPARTLOAD: "1"
N554 		COUNT2BPRODUCED: "1"
N556 		UID: "1"
N558 		GUID: "{526DC9C0-AD32-4745-93F7-8838D873D493}"
N560 	[ENDUID2BPRODUCED]
N562 #COMMENT END
N564 (LC_CONTINUE_CLASH_DETECTION)
N566 (LC_CONTINUE_SIMULATION)
"""
    }
  })
  create_part(TEST_PROJECT_PART_GUIDS[1], {
    u'project_guid': project_data['guid'],
    u'cam_data': {
      u'production_time_simulated': 171677,
      u'loadUID': 2,
      u'reverse':'A',
      u'iso_code': r"""% Pfosten_.nc
N2 (------------------------ General Infos -------------------------)
N4 (LIGNOCAM_VERSION=19.1.2)
N6 (USERPROFIL=C:\ProgramData\lignocam\UserProfil\twmillE_Balteschwiler_M)
N8 (XAM_GUID={DC96C21E-8755-412F-8FAA-B64E5DADBA6A})
N10 (XAM_DATE=08.02.2025 19:01:56)
N12 (XAM_FILENAME=Hackathon.xam)
N14 (LOAD_UID=2)
N16 (LOAD_NAME=Pfosten_)
N18 (LOAD_COMMENT=Bemerkung Charge: .......)
N20 (ISOCODE_DATE=08.02.25 20:10:43)
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
N156 G40 G01 X0.000      Y-678.500   Z0.000      F40500
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
N214 G40 G00 X0.000      Y678.500    Z0.000     
N216 G41 G01 X0.000      Y-0.600     Z0.000      F3000
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
N386 		XAMGUID: "{DC96C21E-8755-412F-8FAA-B64E5DADBA6A}"
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
N412 		GUID: "{8F6541DA-1B6E-4065-B4BF-54AF494025AC}"
N414 	[ENDUID2BPRODUCED]
N416 #COMMENT END
N418 (LC_CONTINUE_CLASH_DETECTION)
N420 (LC_CONTINUE_SIMULATION)
"""
    }
  })

if __name__ == '__main__':
  # delete_prject_by_guid(TEST_PROJECT_GUID)
  # project = create_project(TEST_PROJECT_GUID, {u'name': TEST_PROJECT_NAME})
  # # set_project_name(project.id, TEST_PROJECT_NAME)

  # cam_data = {
  #   u'est_production_time_ms': 123456,
  #   u'load': 1,
  #   u'reverse': 0,
  # }
  # add_cam_data(project.id, cam_data)

  generate_test_data()
  project = get_or_create_project(TEST_PROJECT_GUID)
  print(project.to_dict())

  # # iterate TEST_PART_GUIDS and create parts
  # for part_guid in TEST_PROJECT_PART_GUIDS:
  #   delete_part_by_guid(part_guid)
  #   create_part(part_guid, {u'project_guid': project.to_dict()['guid']})


  # print(project_data['cam_data'])
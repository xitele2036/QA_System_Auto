Develop Envirnoment: Python(x,y)-2.7.10.0

Run AutoTestApp.py to start your testing

1.Test case Management:
  All test cases are managed by Excel, the default test case is "Sanity_Test.xlsx", Here is the the simple description for every field.
  - Case_Available: 1- available for test	
  - Rest_Control: "PAIR" is for rest PAIR, command is in "Rest_Command.xlsx"	
  - IR_Seq: IR command sequence for RedRat control such as "menu,2" means that press menu key and wait for 2s, if the string includes ".xml" which could record with redrat, then it could execute the test sequence.
  - SerialCmd: Serialcommand for DUT serial port	
  - EQ_QD_Control: command for QuantamData control
  - EQ_Streamer_Control: Command for streamer Control (TBD)	
  - Log_Capture:keyword what you want to get from log	
  - Log_Ref:the expected result	
  - PIC_Capture: the picture name do you want to capture.	
  - PIC_Ref: expected reference PIC name
  - Audio_Capture: Audio information from log	
  - Audio_Ref: expected audio result	
  - PIC_Result: comparasion result	
  - Audio_Result: comparation result	
  - Test Result: overall test result

2.Setup the test envirnoment: connect the test equipment to test PC and DUT.
  Test equipment support list: QuantumData generator(UART control) UART for HDMI, RedRat for IR control which need start Redrat hub agent, UniGRAF UCD-2 Vx1 for Vx1 video capture.

3.Edit "AutoTestApp" text file to do configuration before testing such as DUT's IP and Port, DUT's Serial Port, Test PC IP for Red Rat communication and QD generator Serial port.

3.Run AutoTestApp
  (1)select the test cases by double click the test case tree or individual test case that you want to do.
     Example: select SWU_001 - SW upgrade from UART
                     Pair_001 - do system pair
                     Input_004 - Switch source to HDMI4, change timing and pattern, then capture a image with UCD-2 and then do image comparision
   
  (2)Run individual case - select 1 case with case_available=1, and click "Run" button
  (3)Run a group of test case- select multiple test cases which their case_available should be 1, and select Loop to run a group of test cases. Or click "select All" to run all cases.
4. Test Report- Test Result will be written in "Sanity_test.xlsx"



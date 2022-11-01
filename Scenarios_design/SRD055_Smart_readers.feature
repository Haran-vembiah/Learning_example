Feature: SRD077 Setup Smart Reader
  To verify and validate the List of Smart Readers screen and Smart Reader parameters
  verifies:
  1) The menu navigation and "List of Smart Reader" screen header and column header
  2) Display of parameters, its control type and format.
  3) Default value and the list of values of the parameters
  4) validation of the parameters, soft keys and Headers

  Scenario: 44054_User navigation - Setup - Peripherals - Smart Readers
    Given The Resource Smart Readers are available for this Instrument type
    And The user is on the "Menu Tree"
    When The user navigate to the "Smart Readers" via Setup->Peripherals-> Smart Readers
    Then The Terminal displays the "List of Smart Readers" screen

  Scenario: 44054_List of Smart Reader - Screen header
    Given The user is on the "List of Smart Readers" screen
    And The language of Terminal set as "English"
    Then The Terminal displays the screen header as "Smart Readers"

  Scenario Outline: 44054_List of Smart Reader - column headers
    Given The user is on the "List of Smart Readers" screen
    And The language of Terminal set as "English"
    Then The column header <header> is in position <order> from left
    Examples:
      | header     | order |
      | Name       | 1     |
      | Mode       | 2     |
      | Connection | 3     |

  Scenario: 44054_List of Smart Reader - Display of "New" softkey
    Given The user is on the "List of Smart Readers" screen
    And The language of Terminal set as "English"
    Then The softkey "New" is not displayed

  Scenario: 44054_List of Smart Readers - Selecting existing setup entry - Connected
    Given The user is on the "List of Smart Readers" screen
    And The language of Terminal set as "English"
    And The "List of Smart Readers" screen has one Smart Reader setup entry
    And The Smart Reader available in the setup is connected with Instrument
    And The Smart Reader Setup entry available on the list is of mode "Default reader"
    When The User selects the available Smart Reader setup entry from the list
    Then The Terminal displays the "Smart Reader parameter" screen
    And The softkey "Back" is available in "Smart Reader parameter" screen


  Scenario: 44055_Smart Reader parameter screen - Back softkey functionality
    Given The user is on the "Smart Reader parameter" screen
    And The language of Terminal set as "English"
    When The user presses the softkey "Back"
    Then The user is on the "List of Smart Readers" screen

  Scenario Outline: 44055_Smart Reader parameter screen - existing setup entry - Smart reader Connected
    Given The user is on the "Smart Reader parameter" screen
    And The selected Smart Reader is connected with Instrument
    And The Smart Reader Setup entry is of mode "Default reader"
    And The User is in "Smart readers' tab area
    And The language of Terminal set as "English"
    Then The parameter <field_label> is at position <order> from top
    And The <field_label> parameter displays <default_value> as default
    And The parameter <field_label> is in <state> mode
    And The <field_label> parameter has <control_type> UI element
    Examples:
      | field_label | default_value  | state     | control_type | order |
      | Name        | Smart Reader X | DataField | Enabled      | 1     |
      # Have to check for field ID
      | ID          | empty          | DataField | Read-only    | 2     |
      | Connection  |                |           |              | 3     |
      | Mode        | Default reader | ComboBox  | Enabled      | 4     |

  Scenario Outline: 44055_Smart Reader parameter screen - existing setup entry - Smart reader Connected
    Given The user is on the "Smart Reader parameter" screen
    And The selected Smart Reader is connected with Instrument
    And The Smart Reader Setup entry is of mode "Default reader"
    And The User is in 'General' tab area
    And The language of Terminal set as "English"
    Then The parameter <field_label> is at position <order> from top
    And The <field_label> parameter displays <default_value> as default
    And The parameter <field_label> is in <state> mode
    And The <field_label> parameter has <control_type> UI element
    Examples:
      | field_label            | default_value                                  | state     | control_type | order |
      | Chip-ID                | delivered from device – filled upon connection | DataField | Read-only    | 1     |
      | Material number        |                                                | DataField | Enabled      | 2     |
      | Internal ID            |                                                | DataField | Enabled      | 3     |
      | Version                |                                                | DataField | Read-only    | 4     |
      | Last modification time |                                                | DataField | Enabled      | 5     |
      | Modified by            |                                                | DataField | Enabled      | 6     |


  Scenario Outline: 44055_Smart Reader parameter screen - Name - parameter validation
    Given The user is on the "Smart Reader parameter" screen
    And The User is in "Smart readers' tab area
    And The language of Terminal set as "English"
    And The user is on the keyboard screen displayed for the parameter "Name"
    When The user enter the value <input>
    And The user presses the "Ok" button
    Then The parameter <accept_reject> the value entered
    And  <validation_msg> error message displayed
    # validation popup details are available in Req. 31792(SRD017), it was not linked as dependent req.Scenario
    Examples:
      | input                                                                                | accept_reject | validation_msg |
      | Smart Reader 2                                                                       | Accepts       | No             |
      | Smart ReaderSmart ReaderSmart ReaderSmart ReaderSmart ReaderSmart ReaderSmart Reader | Rejects       | Popup ID 100   |
      | Smart Reader 3                                                                       | Accepts       | No             |


  Scenario Outline: 44055_Smart Reader parameter screen - Mode - Parameter validation
    Given The user is on the "Smart Reader parameter" screen
    And The User is in "Smart readers' tab area
    And The language of Terminal set as "English"
    When The User selects the parameter "Mode"
    Then The Terminal displays the value <value> for the parameter "Mode"
    And The User shall able to select the value <value>
    Examples:
      | value             |
      | Default reader    |
      | Permanent pairing |

  Scenario: 44055_Smart Reader parameter screen - Connecting 'Known' smart reader
    Given The user is on the "List of Smart Readers" screen
    And The Smart reader setup entry of Chip ID "123" is available
    And The value of parameter "connection" is "Not Connected"
    When The User connects the Smart Reader with Chip ID "123"
    Then The Terminal displays the "Popup ID 98"


  Scenario: 44055_Smart Reader parameter screen - Known Smart Reader connection - Popup ID 98
    Given The user is on the "popup ID 98"
    And The connecting process of Smart reader with Chip ID "123" is in progress
    When The user presses "Ok" in "popup ID 98"
    Then The user is on the "List of Smart Readers" screen
    And The Smart reader with Chip ID "123" is in connected with the Instrument
    And The value of parameter "Connection" set as "Connected"

  Scenario: 44055_Smart Reader parameter screen - Connecting 'UnKnown' smart reader
    Given The user is on the "List of Smart Readers" screen
    And The Smart reader setup entry of Chip ID "124" is not available in Setup
    And No Smart reader setup entry exist with Mode "Default Reader"
    When The User connects the Smart Reader with Chip ID "124"
    Then The Terminal displays the "Popup ID 97"

   # Presumes that, during connection of Unknown Smart Reader, it shows Popup 97 and then Popup 99
  Scenario: 44055_44053_Smart Reader parameter screen - UnKnown Smart Reader connection - Popup ID 97
    Given The user is on the "popup ID 97"
    And The connecting process of Smart reader with Chip ID "124" is in progress
    When The user presses "Ok" in "popup ID 97"
    Then The Terminal displays the "Popup ID 99"

  Scenario: 44055_44053_Smart Reader parameter screen - UnKnown Smart Reader connection - Popup ID 99 - Default reader
    Given The user is on the "popup ID 99"
    And The connecting process of Smart reader with Chip ID "124" is in progress
    And The Smart reader setup entry of Chip ID "124" is not available in Setup
    When The user presses "Yes" in "popup ID 99"
    Then The user is on the "List of Smart Readers" screen
    And The Smart reader setup entry created for Chip ID "124"
    And The parameter "Mode" of setup entry created for Chip ID "124" set as "Default Reader"
    And The value of parameter "Connection" set as "Connected"

  Scenario: 44055_44053_Smart Reader parameter screen - UnKnown Smart Reader connection - Mode 'Permanent pairing'
    Given The Smart reader setup entry of Chip ID "xxx" is not available in Setup
    And The Smart Readers list has "1" setup entry of mode "Default reader"
    And The Smart Readers list has "2" setup entries of mode "Permanent pairing"
    And The connecting process of Smart reader with Chip ID "xxx" is in progress
    And The User pressed 'OK' in Popup ID 97
    And The Terminal displays the "Popup ID 99"
    When The user presses "No" in "popup ID 99"
    Then The user is on the "List of Smart Readers" screen
    And The Smart reader setup entry created for Chip ID "xxx"
    And The parameter "Mode" of setup entry created for Chip ID "xxx" set as "Permanent pairing"
    And The Smart Readers list has "1" setup entry of mode "Default reader"
    And The Smart Readers list has "3" setup entries of mode "Permanent pairing"

  Scenario: 44055_44053_Smart Reader parameter screen - UnKnown Smart Reader connection - Mode 'Default reader' when there is one default reader in list
    Given The Smart reader setup entry of Chip ID "xxx" is not available in Setup
    And The Smart Readers list has setup entry "Reader x" with mode "Default reader"
    And The Smart Readers list has "2" setup entries of mode "Permanent pairing"
    And The connecting process of Smart reader with Chip ID "xxx" is in progress
    And The User pressed 'OK' in Popup ID 97
    And The Terminal displays the "Popup ID 99"
    When The user presses "Yes" in "popup ID 99"
    Then The user is on the "List of Smart Readers" screen
    And The Smart reader setup entry created for Chip ID "xxx"
    And The parameter "Mode" of setup entry "Reader x" set as "Permanent pairing"
    And The parameter "Mode" of setup entry created for Chip ID "xxx" set as "Default reader"
    And The Smart Readers list has "1" setup entry of mode "Default reader"
    And The Smart Readers list has "3" setup entries of mode "Permanent pairing"


  # To verify the visibility of softkeys "Discard" and "Save"
  Scenario Outline: 44055_30327_"Smart Reader parameter" screen - Unsaved changes - Softkeys verification
    Given The user is on the "Smart Reader parameter" screen
    And The language of Terminal set as "English"
    And The user is on <tab_name> tab area
    When Parameters in <tab_name> tab area has new values
    Then The softkey "Cancel" is visible at position "1"
    And The softkey "Save" is visible at position "5"
    And The User cannot access the other tabs
    Examples:
      | tab_name      |
      | Smart readers |
      | General       |

  Scenario Outline: 44055_30327_"Smart Reader parameter" screen - Unsaved changes - Softkeys verification
    Given The user is on the "Smart Reader parameter" screen
    And The language of Terminal set as "English"
    And The user is on <tab_name> tab area
    When Parameters in <tab_name> tab area has new values
    Then The softkey "Cancel" is visible at position "1"
    And The softkey "Save" is visible at position "5"
    And The User cannot access the other tabs
    Examples:
      | tab_name      |
      | Smart readers |
      | General       |

  Scenario Outline: 44055_30320(Discard)_"Smart Reader parameter" screen - "Discard Changes" popup
    Given The user is on the "Smart Reader parameter" screen
    And The language of Terminal set as "English"
    And The user is on <tab_name> tab area
    And Parameters in <tab_name> tab area has new values
    When The user presses the softkey "Discard"
    Then The Terminal displays the "popup ID 16" on the screen
    Examples:
      | tab_name      |
      | Smart readers |
      | General       |

  Scenario: 44055_"Smart Reader parameter" screen - "Discard Changes"_"No"
    Given The user is on the "popup ID 16"
    When The user presses "No" in "popup ID 16"
    Then The user is on the "Smart Reader parameter" screen
    And The parameters are with updated values

  Scenario Outline: 44055_30320(Discard)_"Smart Reader parameter" screen - "Discard Changes"- Yes
    Given The user is on the "Smart Reader parameter" screen
    And The language of Terminal set as "English"
    And The user is on <tab_name> tab area
    And Parameters in <tab_name> tab area has new values
    And The User cannot access the other tabs
    And The user is on the "popup ID 16"
    When The user presses "Yes" in the "popup ID 16"
    Then The updated changes are discarded
    And The old values of the parameters are retained
    And The user is on <tab_name> tab area
    And The User can able to access the other tabs
    Examples:
      | tab_name      |
      | Smart readers |
      | General       |

  Scenario Outline: 44055_30326(Save)_"Smart Reader parameter" screen - "Save" softkey functionality
    Given The user is on the "Smart Reader parameter" screen
    And The language of Terminal set as "English"
    And The user is on <tab_name> tab area
    And Parameters in <tab_name> tab area has new values
    And The User cannot access the other tabs
    When The user presses the softkey "Save"
    Then The Parameters on <tab_name> tab area is saved with updated values
    And The user is on <tab_name> tab area
    And The User can able to access the other tabs
    Examples:
      | tab_name      |
      | Smart readers |
      | General       |

  Scenario: 44055_30326(Save)_"Smart Reader parameter" screen - "Save" softkey validation
    Given  The "Smart Reader list" screen has "Reader X" of mode "Default Reader"
    And  The "Smart Reader list" screen has "Reader y" of mode "Permanent pairing"
    And The "Reader Y" selected from "Smart Reader list" screen
    And The user is on the "Smart Reader parameter" screen of "Reader Y"
    And The language of Terminal set as "English"
    And The user is on Smart readers tab area
    When The User set the value of parameter "Mode" as "Default Reader"
    And The User presses the softkey "Save"
    Then The parameter "Mode" of "Reader Y" set as "Default reader"
    And The parameter "Mode" of "Reader X" set as "Permanent pairing"

  Scenario Outline: 44055_30323_"Smart Reader parameter" screen - Delete - Softkeys verification
    Given The user is on the "Smart Reader parameter" screen of existing Smart reader entry
    And The selected "Smart Reader" is <connected> with the Instrument
    And The language of Terminal set as "English"
    Then The softkey "Delete" is visible at position "3"
    And The softkey "Delete" is in <state> state
    Examples:
      | connected     | state    |
      | Connected     | Disbaled |
      | Not Connected | Enabled  |

  Scenario: 44055_30323_"Smart Reader parameter" screen - Delete - Softkeys Validation
    Given The user is on the "Smart Reader parameter" screen of existing Smart reader entry
    And The selected "Smart Reader" is "Not connected" with the Instrument
    And The language of Terminal set as "English"
    And The softkey "Delete" is visible at position "3"
    And The softkey "Delete" is in "Enabled" state
    When The User Presses the softkey "Delete"
    Then The Terminal displays popup "Popup ID 18" on the screen

  Scenario: 44055_30323_"Smart Reader parameter" screen - "Delete"_"No"
    Given The user is on the "Smart Reader parameter" screen of existing Smart reader entry
    And The user is on the "popup ID 18"
    When The user presses "No" in "popup ID 18"
    Then The selected "Smart Reader" not deleted
    And The user is on the "Smart Reader parameter" screen of existing Smart reader entry
    And The parameters are with updated values

  Scenario: 44055_30323_"Smart Reader parameter" screen - "Delete"_"Yes"
    Given The user is on the "Smart Reader parameter" screen of existing Smart reader entry
    And The user is on the "popup ID 18"
    When The user presses "No" in "popup ID 18"
    Then The selected "Smart Reader" deleted from the list
    And The selected "Smart Reader" is not available in the "List of Smart Readers" screen

  # Resource functionalities of “PnP-USB Peripherals (>1) mentioned in requirement: 46369
  # For "Remove" a shared resource, mentioned a comment: Current state: Peripherals will be strictly local. #-> No ‘Remove’ needed
  # For "Restore a deleted resource". mentioned in a comment: TBD later- Wait for LXC HR Instrument management
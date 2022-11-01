Feature: SRD055 Setup Peripherals - LabX and Network
  To verify and validate the LabX and Network screen and 'LabX and Network' parameters
  verifies:
  1) The menu navigation and "LabX and Network" screen header
  2) Display of parameters, its control type and format.
  3) Default value and the list of values of the parameters
  4) validation of the parameters, soft keys and Headers

  Scenario: 36297_User navigation - Setup - Peripherals  - LabX and Network
    Given The Peripherals "LabX and Network" is available for this Instrument type
    And The user is on the "Menu Tree"
    When The user navigate to the "LabX and Network" via Setup->Peripherals-> LabX and Network
    Then The Terminal displays the "LabX and Network" screen

  Scenario: 36302_LabX and Network - Screen header
    Given The user is on the "LabX and Network" screen
    And The language of Terminal set as "English"
    Then The Terminal displays the screen header as "LabX and Network"

  Scenario Outline: 36302_LabX and Network - Tabs verification
    Given The user is on the "LabX and Network" screen
    And The language of Terminal set as "English"
    Then The Tab <tab_name> is available on "LabX and Network" screen
    Examples:
      | tab_name         |
      | LabX settings    |
      | Network settings |
      | Network storage  |
      | Remote interface |

  Scenario: 44050_'LabX settings' tab - Navigation
    Given The user is on the "LabX and Network" screen
    And The language of Terminal set as "English"
    When The User presses the tab "LabX settings"
    Then The Terminal displays "LabX settings" tab area

  #TODO: Parameters on the 'LabX settings' tab area are in draft state - TBD

  Scenario: 36303_'Network settings' tab - Navigation
    Given The user is on the "LabX and Network" screen
    And The language of Terminal set as "English"
    When The User presses the tab "Network settings"
    Then The Terminal displays "Network settings" tab area

  Scenario Outline: 36303_'Network settings' tab area - parameters - Default values
    Given The user is on the "LabX and Network" screen
    And The user is on "Network settings" tab area
    And The language of Terminal set as "English"
    Then The parameter <field_label> is at position <order> from top
    And The <field_label> parameter displays <default_value> as default
    And The parameter <field_label> is in <state> mode
    And The <field_label> parameter has <control_type> UI element
    Examples:
      | field_label                       | default_value             | control_type | state     | order |
      | IP type                           | IPv4                      | ComboBox     | Enabled   | 1     |
      | Obtain IPv4 address automatically | Y                         | BOOLEAN      | Enabled   | 2     |
      | IPv4 address                      | [Filled in automatically] | UNKNOWN      | Read-only | 3     |
      | IPv4 subnet mask                  | [Filled in automatically] | UNKNOWN      | Read-only | 4     |
      | IPv4 standard gateway             | [Filled in automatically] | UNKNOWN      | Read-only | 5     |

  Scenario Outline: 36303_'Network settings' tab area - IP type - Parameter validation
    Given The user is on the "LabX and Network" screen
    And The user is on "Network settings" tab area
    And The language of Terminal set as "English"
    When The User selects the parameter "IP type"
    Then The Terminal displays the value <value> for the parameter "IP type"
    And The User shall able to select the value <value>
    Examples:
      | value |
      | IPv4  |
      | IPv6  |

  Scenario Outline: 36303_'Network settings' tab area - parameters - Default values - IP type "IPv6"
    Given The user is on the "LabX and Network" screen
    And The user is on "Network settings" tab area
    And The language of Terminal set as "English"
    And The parameter "IP type" set as "IPv6"
    Then The parameter <field_label> is at position <order> from top
    And The <field_label> parameter displays <default_value> as default
    And The parameter <field_label> is in <state> mode
    And The <field_label> parameter has <control_type> UI element
    Examples:
      | field_label  | default_value            | control_type | state     | order |
      | IPv6 address | Filled in automatically] | UNKNOWN      | Read-only | 2     |


  Scenario Outline: 36303_'Network settings' tab area - Obtain IPv4 address automatically  - Parameter validation
    Given The user is on the "LabX and Network" screen
    And The user is on "Network settings" tab area
    And The language of Terminal set as "English"
    And The parameter "IP type" set as "IPv4"
    When The User <selection> the parameter "Obtain IPv4 address automatically"
    Then The Terminal <Selection_result> the parameter "Obtain IPv4 address automatically"
    Examples:
      | selection | Selection_result |
      | Enables   | Enabled          |
      | Disables  | Disabled         |

  # TODO : TBD - For validation of parameters with IP type = IPv4 and Obtain IPv4 address automatically = Y
  # Because, there s no information from where these parameters are automatically filled in.
  # and the Parameters are IPv4 address, IPv4 subnet mask, IPv4 standard gateway

  Scenario Outline: 36303_'Network settings' tab area - parameters Default values - "Ip type = IPv4" and "Obtain IPv4 address automatically = N"
    Given The user is on the "LabX and Network" screen
    And The user is on "Network settings" tab area
    And The parameter "Ip type" set as "IPv4"
    And The parameter "Obtain IPv4 address automatically" set as "N"
    And The language of Terminal set as "English"
    Then The parameter <field_label> is at position <order> from top
    And The <field_label> parameter displays <default_value> as default
    And The parameter <field_label> is in <state> mode
    And The <field_label> parameter has <control_type> UI element
    Examples:
      | field_label           | default_value | control_type | state   | order |
      | IPv4 address          | 192.168.80.2  | DataField    | Enabled | 3     |
      | IPv4 subnet mask      | 255.255.255.0 | DataField    | Enabled | 4     |
      | IPv4 standard gateway | 0.0.0.0       | DataField    | Enabled | 5     |


  Scenario Outline: 36303_'Network settings' tab area - IPv4 address - parameter validation
    Given The user is on the "LabX and Network" screen
    And The user is on "Network settings" tab area
    And The parameter "Ip type" set as "IPv4"
    And The parameter "Obtain IPv4 address automatically" set as "N"
    And The language of Terminal set as "English"
    And The user is on the keyboard screen displayed for the parameter "IPv4 address"
    When The user enter the value <input>
    And The user presses the "Ok" button
    Then The parameter <accept_reject> the value entered
    And  <validation_msg> error message displayed
    # validation popup details are available in Req. 31792(SRD017), it was not linked as dependent req.Scenario
    Examples:
      | input           | accept_reject | validation_msg |
      | 192.168.80.5    | Accepts       | No             |
      | 192.168.80.2234 | Rejects       | Popup ID 100   |
      | 192.168.90.2    | Accepts       | No             |

  Scenario Outline: 36303_'Network settings' tab area - IPv4 subnet mask - parameter validation
    Given The user is on the "LabX and Network" screen
    And The user is on "Network settings" tab area
    And The parameter "Ip type" set as "IPv4"
    And The parameter "Obtain IPv4 address automatically" set as "N"
    And The language of Terminal set as "English"
    And The user is on the keyboard screen displayed for the parameter "IPv4 subnet mask"
    When The user enter the value <input>
    And The user presses the "Ok" button
    Then The parameter <accept_reject> the value entered
    And  <validation_msg> error message displayed
    # validation popup details are available in Req. 31792(SRD017), it was not linked as dependent req.Scenario
    Examples:
      | input            | accept_reject | validation_msg |
      | 255.255.255.2    | Accepts       | No             |
      | 255.255.255.1234 | Rejects       | Popup ID 100   |
      | 255.255.255.1    | Accepts       | No             |

  Scenario Outline: 36303_'Network settings' tab area - IPv4 standard gateway - parameter validation
    Given The user is on the "LabX and Network" screen
    And The user is on "Network settings" tab area
    And The parameter "Ip type" set as "IPv4"
    And The parameter "Obtain IPv4 address automatically" set as "N"
    And The language of Terminal set as "English"
    And The user is on the keyboard screen displayed for the parameter "IPv4 standard gateway"
    When The user enter the value <input>
    And The user presses the "Ok" button
    Then The parameter <accept_reject> the value entered
    And  <validation_msg> error message displayed
    # validation popup details are available in Req. 31792(SRD017), it was not linked as dependent req.Scenario
    Examples:
      | input            | accept_reject | validation_msg |
      | 0.0.0.0          | Accepts       | No             |
      | 255.255.255.1234 | Rejects       | Popup ID 100   |
      | 255.255.255.1    | Accepts       | No             |


  Scenario: 36304_'Network storage' tab - Navigation
    Given The user is on the "LabX and Network" screen
    And The language of Terminal set as "English"
    When The User presses the tab "Network storage"
    Then The Terminal displays "Network storage" tab area


  Scenario Outline: 36304_'Network storage' tab area - parameters - Default values
    Given The user is on the "LabX and Network" screen
    And The user is on "Network storage" tab area
    And The language of Terminal set as "English"
    Then The parameter <field_label> is at position <order> from top
    And The <field_label> parameter displays <default_value> as default
    And The parameter <field_label> is in <state> mode
    And The <field_label> parameter has <control_type> UI element
    Examples:
      | field_label        | default_value | control_type | state     | order |
      | Transfer via       | Network share | UNKNOWN      | Read-only | 1     |
      | Server PC          | empty         | DataField    | Enabled   | 2     |
      | Share name         | empty         | DataField    | Enabled   | 3     |
      | Domain             | empty         | DataField    | Enabled   | 4     |
      | User name          | empty         | DataField    | Enabled   | 5     |
      | Password           | ******        | DataField    | Enabled   | 6     |
      | Target folder      | Titration     | DataField    | Enabled   | 7     |
      | First folder level | None          | ComboBox     | Enabled   | 8     |

  Scenario Outline: 36304_'Network storage' tab area - parameters Default values - "First folder level = User name"
    Given The user is on the "LabX and Network" screen
    And The user is on "Network storage" tab area
    And The language of Terminal set as "English"
    And The parameter "First folder level" set as <Param_value>
      | User name     |
      | Instrument ID |
      | Date          |
      | Method ID     |
    Then The parameter <field_label> is at position <order> from top
    And The <field_label> parameter displays <default_value> as default
    And The parameter <field_label> is in <state> mode
    And The <field_label> parameter has <control_type> UI element
    Examples: Default parameter
      # This parameter applies for all the values given in the above data table
      | field_label         | default_value | control_type | state   | order |
      | Second folder level | None          | ComboBox     | Enabled | 9     |


  Scenario Outline: 36304_'Network storage' tab area - Server PC - parameter validation
    Given The user is on the "LabX and Network" screen
    And The user is on "Network storage" tab area
    And The language of Terminal set as "English"
    And The user is on the keyboard screen displayed for the parameter "Server PC"
    When The user enter the value <input>
    And The user presses the "Ok" button
    Then The parameter <accept_reject> the value entered
    And  <validation_msg> error message displayed
    # validation popup details are available in Req. 31792(SRD017), it was not linked as dependent req.Scenario
    # with SRD017, Popup ID 100 applies for all parameter validation
    # But in SRD055, with the constraints "^\/:*?"|<>[]" its is mentioned Popup ID 89 - TBD, also the there is no condition defined and not mentioned
      # any specific parameter there
    Examples:
      # Constraints for value ranga: any, except: ^\/:*?"|<>[]
      | input   | accept_reject | validation_msg |
      | valid   | Accepts       | No             |
      | invalid | Rejects       | Popup ID 89    |
      | valid   | Accepts       | No             |

  Scenario Outline: 36304_'Network storage' tab area - Share name - parameter validation
    Given The user is on the "LabX and Network" screen
    And The user is on "Network storage" tab area
    And The language of Terminal set as "English"
    And The user is on the keyboard screen displayed for the parameter "Share name"
    When The user enter the value <input>
    And The user presses the "Ok" button
    Then The parameter <accept_reject> the value entered
    And  <validation_msg> error message displayed
    # validation popup details are available in Req. 31792(SRD017), it was not linked as dependent req.Scenario
    # with SRD017, Popup ID 100 applies for all parameter validation
    # But in SRD055, with the constraints "^\/:*?"|<>[]" its is mentioned Popup ID 89 - TBD, also the there is no condition defined and not mentioned
      # any specific parameter there
    Examples:
      # Constraints for value ranga: any, except: ^\/:*?"|<>[]
      | input   | accept_reject | validation_msg |
      | valid   | Accepts       | No             |
      | invalid | Rejects       | Popup ID 100   |
      | valid   | Accepts       | No             |

  Scenario Outline: 36304_'Network storage' tab area - Domain - parameter validation
    Given The user is on the "LabX and Network" screen
    And The user is on "Network storage" tab area
    And The language of Terminal set as "English"
    And The user is on the keyboard screen displayed for the parameter "Domain"
    When The user enter the value <input>
    And The user presses the "Ok" button
    Then The parameter <accept_reject> the value entered
    And  <validation_msg> error message displayed
    # validation popup details are available in Req. 31792(SRD017), it was not linked as dependent req.Scenario
    Examples:
      | input   | accept_reject | validation_msg |
      | valid   | Accepts       | No             |
      | invalid | Rejects       | Popup ID 100   |
      | valid   | Accepts       | No             |

  Scenario Outline: 36304_'Network storage' tab area - User name - parameter validation
    Given The user is on the "LabX and Network" screen
    And The user is on "Network storage" tab area
    And The language of Terminal set as "English"
    And The user is on the keyboard screen displayed for the parameter "User name"
    When The user enter the value <input>
    And The user presses the "Ok" button
    Then The parameter <accept_reject> the value entered
    And  <validation_msg> error message displayed
    # validation popup details are available in Req. 31792(SRD017), it was not linked as dependent req.Scenario
    Examples:
      | input   | accept_reject | validation_msg |
      | valid   | Accepts       | No             |
      | invalid | Rejects       | Popup ID 100   |
      | valid   | Accepts       | No             |

  Scenario Outline: 36304_'Network storage' tab area - Password - parameter validation
    Given The user is on the "LabX and Network" screen
    And The user is on "Network storage" tab area
    And The language of Terminal set as "English"
    And The user is on the keyboard screen displayed for the parameter "Password"
    When The user enter the value <input>
    And The user presses the "Ok" button
    Then The parameter <accept_reject> the value entered
    And  <validation_msg> error message displayed
    # validation popup details are available in Req. 31792(SRD017), it was not linked as dependent req.Scenario
    Examples:
      | input   | accept_reject | validation_msg |
      | valid   | Accepts       | No             |
      | invalid | Rejects       | Popup ID 100   |
      | valid   | Accepts       | No             |


  Scenario Outline: 36304_'Network storage' tab area - Target folder - parameter validation
    Given The user is on the "LabX and Network" screen
    And The user is on "Network storage" tab area
    And The language of Terminal set as "English"
    And The user is on the keyboard screen displayed for the parameter "Target folder"
    When The user enter the value <input>
    And The user presses the "Ok" button
    Then The parameter <accept_reject> the value entered
    And  <validation_msg> error message displayed
    # validation popup details are available in Req. 31792(SRD017), it was not linked as dependent req.Scenario
    Examples:
      | input   | accept_reject | validation_msg |
      | valid   | Accepts       | No             |
      | invalid | Rejects       | Popup ID 100   |
      | valid   | Accepts       | No             |

  Scenario Outline: 36304_'Network storage' tab area - First folder level - Parameter validation
    Given The user is on the "LabX and Network" screen
    And The user is on "Network storage" tab area
    And The language of Terminal set as "English"
    When The User selects the parameter "First folder level"
    Then The Terminal displays the value <value> for the parameter "First folder level"
    And The User shall able to select the value <value>
    Examples:
      | value         |
      | None          |
      | User name     |
      | Instrument ID |
      | Method ID     |

  Scenario Outline: 36304_'Network storage' tab area - Second folder level - Parameter validation
    Given The user is on the "LabX and Network" screen
    And The user is on "Network storage" tab area
    And The language of Terminal set as "English"
    And The parameter "First folder level" set as <Param_value>
      | User name     |
      | Instrument ID |
      | Date          |
      | Method ID     |
    When The User selects the parameter "Second folder level"
    Then The Terminal displays the value <value> for the parameter "Second folder level"
    And The User shall able to select the value <value>
    Examples:
     # These values of parameter "Second folder level" applies for all the values given in the above data table
      | value         |
      | None          |
      | User name     |
      | Instrument ID |
      | Method ID     |

  Scenario Outline: 36304_'Network storage' tab area - Connection test - Softkey verification
    Given The user is on the "LabX and Network" screen
    And The user is on "Network storage" tab area
    And The language of Terminal set as "English"
    And The "Network storage" tab area has <changes>
    Then The softkey "Connection test" is visible at position "3"
    And  The softkey "Connection test" is in <state> state
    Examples:
      | changes            | state    |
      | no pending changes | Enabled  |
      | pending changes    | Disabled |

  Scenario Outline: 36304_'Network storage' tab area - Connection test - Softkey Validation
    Given The user is on the "LabX and Network" screen
    And The user is on "Network storage" tab area
    And The language of Terminal set as "English"
    And The "Network storage" tab area has no pending changes
    And Parameters has <data> data for connection
    When The User presses the softkey "Connection test"
    Then The Terminal displays the <popup> in the screen
    Examples:
      # PopUp ID's for Validation depends on the reason of failure
      # Mentioned as popup ID 94a-f for not successful connection
      # No information on which failure, what popups should be displayed
      | data               | popup        |
      | Valid              | Popup ID 93  |
      | invalid Server PC  | Popup ID 94a |
      | invalid Share name | Popup ID 94b |
      | invalid Domain     | Popup ID 93c |
      | invalid User name  | Popup ID 94d |
      | invalid Password   | Popup ID 94d |
      | invalid            | Popup ID 94e |
      | invalid            | Popup ID 94f |

  #TODO: Parameters on the 'Remote interface' tab area are in draft state - TBD

  # To verify the visibility of softkeys "Discard" and "Save"
  Scenario Outline: 36302_30327_'LabX and Network' screen - Unsaved changes - Softkeys verification
    Given The user is on the "LabX and Network" screen
    And The language of Terminal set as "English"
    And The user is on <tab_name> tab area
    When Parameters in <tab_name> tab area has new values
    Then The softkey "Cancel" is visible at position "1"
    And The softkey "Save" is visible at position "5"
    And The User cannot access the other tabs
    Examples:
      | tab_name         |
      | LabX settings    |
      | Network settings |
      | Network storage  |
      | Remote interface |

  Scenario Outline: 36302_30320(Discard)_'LabX and Network' screen- "Discard Changes" popup
    Given The user is on the "LabX and Network" screen
    And The language of Terminal set as "English"
    And The user is on <tab_name> tab area
    And Parameters in <tab_name> tab area has new values
    When The user presses the softkey "Discard"
    Then The Terminal displays the "popup ID 16" on the screen
    Examples:
      | tab_name         |
      | LabX settings    |
      | Network settings |
      | Network storage  |
      | Remote interface |

  Scenario: 36302_'LabX and Network' screen- - "Discard Changes"_"No"
    Given The user is on the "popup ID 16"
    When The user presses "No" in "popup ID 16"
    Then The user is on the "LabX and Network" screen
    And The parameters are with updated values

  Scenario Outline: 36302_30320(Discard)_'LabX and Network' screen- "Discard Changes"- Yes
    Given The user is on the "LabX and Network" screen
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
      | tab_name         |
      | LabX settings    |
      | Network settings |
      | Network storage  |
      | Remote interface |

  Scenario Outline: 36302_30326(Save)_'LabX and Network' screen - "Save" softkey functionality
    Given The user is on the "LabX and Network" screen
    And The language of Terminal set as "English"
    And The user is on <tab_name> tab area
    And Parameters in <tab_name> tab area has new values
    And The User cannot access the other tabs
    When The user presses the softkey "Save"
    Then The Parameters on <tab_name> tab area is saved with updated values
    And The user is on <tab_name> tab area
    And The User can able to access the other tabs
    Examples:
      | tab_name         |
      | LabX settings    |
      | Network settings |
      | Network storage  |
      | Remote interface |


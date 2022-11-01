Feature: SRD055 Setup Peripherals - Balances
  To verify and validate the Balances screen and 'Balances' parameters
  verifies:
  1) The menu navigation and "Balances" screen header
  2) Display of parameters, its control type and format.
  3) Default value and the list of values of the parameters
  4) validation of the parameters, soft keys and Headers

  Scenario: 44060_User navigation - Setup - Peripherals  - Balances
    Given The Peripherals "Balances" is available for this Instrument type
    And The user is on the "Menu Tree"
    When The user navigate to the "Balances" via Setup->Peripherals-> Balances
    Then The Terminal displays the "Balance parameter" screen


  Scenario: 44061_Balance parameter screen - Screen header
    Given The user is on the "Balance parameter" screen
    And The language of Terminal set as "English"
    Then The Terminal displays the screen header as "Balances"

  Scenario Outline: 44061_Balance parameter screen - Tabs verification
    Given The user is on the "Balance" screen
    And The language of Terminal set as "English"
    Then The Tab <tab_name> is available on "Balance parameter" screen
    Examples:
      | tab_name |
      | Balance  |
      | General  |

  Scenario: 44061_'Balance' tab area - Navigation
    Given The user is on the "Balance parameter" screen
    And The language of Terminal set as "English"
    When The User presses the tab "Balance"
    Then The Terminal displays "Balances" tab area

  Scenario Outline: 44061_"Balance parameter" screen - parameters - Default values - "Balances' tab area
    Given The user is on the "Balance parameter" screen
    And The user is on "Balance" tab area
    And The language of Terminal set as "English"
    Then The parameter <field_label> is at position <order> from top
    And The <field_label> parameter displays <default_value> as default
    And The parameter <field_label> is in <state> mode
    And The <field_label> parameter has <control_type> UI element
    Examples:
      | field_label      | default_value | control_type | state     | order |
      | Category         | Mettler USB   | ComboBox     | Enabled   | 1     |
      # Have to check for field ID, related to LCM
      | ID               |               |              |           | 2     |
      | Connection       |               |              |           | 3     |
      | Model            |               | UNKNOWN      | Read-only | 4     |
      | Software version |               | UNKNOWN      | Read-only | 5     |

  Scenario: 44061_'General' tab area - Navigation
    Given The user is on the "Balance parameter" screen
    And The language of Terminal set as "English"
    When The User presses the tab "General"
    Then The Terminal displays "General" tab area

  Scenario Outline: 44061_"Balance parameter" screen - parameters - Default values - "General' tab area
    Given The user is on the "Balance parameter" screen
    And The user is on "General" tab area
    And The language of Terminal set as "English"
    Then The parameter <field_label> is at position <order> from top
    And The <field_label> parameter displays <default_value> as default
    And The parameter <field_label> is in <state> mode
    And The <field_label> parameter has <control_type> UI element
    Examples:
      # Except Serial number all the other parameters are applicable only for LCM
      | field_label            | default_value                                       | control_type | state     | order |
      | Serial number          | delivered from device chip – filled upon connection | DataField    | Read-only | 1     |
      | Internal ID            |                                                     | DataField    | Enabled   | 2     |
      | Version                |                                                     | DataField    | Read-only | 3     |
      | Last modification time |                                                     | DataField    | Enabled   | 4     |
      | Modified by            |                                                     | DataField    | Enabled   | 5     |

  Scenario Outline: 44061_"Balance parameter" screen - Category - Parameter validation
    Given The user is on the "Balance parameter" screen
    And The user is on "Balance" tab area
    And The language of Terminal set as "English"
    When The User selects the parameter "Category"
    Then The Terminal displays the value <value> for the parameter "Category"
    And The User shall able to select the value <value>
    Examples:
      # TODO: Category "Mettler USB Juno" may included - TBD, Comment in SRD
      | value          |
      | Mettler USB    |
      | Mettler RS-232 |

  # This parameter applies only for LCM as mentioned by Marcel in Bug: 46947
  Scenario: 44061_"Balance parameter" screen - ID - parameter validation
    Given The user is on the "Balance parameter" screen
    And The user is on "Balance" tab area
    Then The parameter "ID" has the value "Balance ID"

  Scenario: 44061_"Balance parameter" screen - Connection - parameter validation - Not connected with Balance
    Given The user is on the "Balance parameter" screen
    And The user is on "Balance" tab area
    And The Instrument not connected with Balance
    Then The parameter "Connection" has the value "Not connected"

  Scenario: 44061_"Balance parameter" screen - Connection - parameter validation - connected with Balance
    Given The user is on the "Balance parameter" screen
    And The user is on "Balance" tab area
    And The Instrument connected with supported type of Balance
    Then The parameter "Connection" has the value "Connected"

  Scenario: 44061_"Balance parameter" screen - Model - parameter validation - Not connected with Balance
    Given The user is on the "Balance parameter" screen
    And The user is on "Balance" tab area
    And The Instrument not connected with Balance
    Then The parameter "Model" is "Null"

  Scenario: 44061_"Balance parameter" screen - Model - parameter validation - connected with Balance
    Given The user is on the "Balance parameter" screen
    And The user is on "Balance" tab area
    And The Instrument connected with Balance model "XSR"
    Then The parameter "Model" has the value "XSR"

  Scenario: 44061_"Balance parameter" screen - Software version - parameter validation - Not connected with Balance
    Given The user is on the "Balance parameter" screen
    And The user is on "Balance" tab area
    And The Terminal not connected with Balance
    Then The parameter "Software version" is "Null"

  Scenario Outline: 44061_"Balance parameter" screen - parameters - Default values - Category = Mettler RS-232
    Given The user is on the "Balance parameter" screen
    And The user is on "Balance" tab area
    And The language of Terminal set as "English"
    Then The parameter <field_label> is at position <order> from top
    And The <field_label> parameter displays <default_value> as default
    And The parameter <field_label> is in <state> mode
    And The <field_label> parameter has <control_type> UI element
    Examples:
      | field_label      | default_value | control_type | state     | order |
      | Category         | Mettler USB   | ComboBox     | Enabled   | 1     |
      # Have to check for field ID, related to LCM
      | ID               |               |              |           | 2     |
      | Connection       |               |              |           | 3     |
      | Model            |               | UNKNOWN      | Read-only | 4     |
      | Software version |               | UNKNOWN      | Read-only | 5     |
      | Baud rate        | 9600          | ComboBox     | Enabled   | 6     |
      | Data bit         | 8             | ComboBox     | Enabled   | 7     |
      | Stop bit         | 1             | ComboBox     | Enabled   | 8     |
      | Parity           | None          | ComboBox     | Enabled   | 9     |
      | Flow control     | Off           | ComboBox     | Enabled   | 10    |


  Scenario Outline: 44061_"Balance parameter" screen - Baud rate - parameter validation
    Given The user is on the "Balance parameter" screen
    And The user is on "Balances" tab area
    And The language of Terminal set as "English"
    When The User selects the parameter "Baud rate"
    Then The Terminal displays the value <value> for the parameter "Baud rate"
    And The User shall able to select the value <value>
    Examples:
      | value  |
      | 1200   |
      | 2400   |
      | 4800   |
      | 9600   |
      | 19200  |
      | 38400  |
      | 57600  |
      | 115200 |

  Scenario Outline: 44061_"Balance parameter" screen - Data bit - parameter validation
    Given The user is on the "Balance parameter" screen
    And The user is on "Balances" tab area
    And The language of Terminal set as "English"
    When The User selects the parameter "Data bit"
    Then The Terminal displays the value <value> for the parameter "Data bit"
    And The User shall able to select the value <value>
    Examples:
      | value |
      | 7     |
      | 8     |

  Scenario Outline: 44061_"Balance parameter" screen - Stop bit - parameter validation
    Given The user is on the "Balance parameter" screen
    And The user is on "Balances" tab area
    And The language of Terminal set as "English"
    When The User selects the parameter "Stop bit"
    Then The Terminal displays the value <value> for the parameter "Stop bit"
    And The User shall able to select the value <value>
    Examples:
      | value |
      | 1     |
      | 2     |

  Scenario Outline: 44061_"Balance parameter" screen - Parity - parameter validation
    Given The user is on the "Balance parameter" screen
    And The user is on "Balances" tab area
    And The language of Terminal set as "English"
    When The User selects the parameter "Parity"
    Then The Terminal displays the value <value> for the parameter "Parity"
    And The User shall able to select the value <value>
    Examples:
      | value |
      | None  |
      | Even  |
      | Odd   |

  Scenario Outline: 44061_"Balance parameter" screen - Flow control - parameter validation
    Given The user is on the "Balance parameter" screen
    And The user is on "Balances" tab area
    And The language of Terminal set as "English"
    When The User selects the parameter "Flow control"
    Then The Terminal displays the value <value> for the parameter "Flow control"
    And The User shall able to select the value <value>
    Examples:
      | value    |
      | Off      |
      | RTS/CTS  |
      | XON/XOFF |

  # plug-in type ‘PnP USB Peripheral (=1) for Balances
  # Connecting with Wrong category and right category verification
  Scenario Outline: 45505_44085_Resource rules - Connecting Balances - Category fits and wrong category
    Given The user is on the "Balance parameter" screen
    And The user is on "Balances" tab area
    And The language of Terminal set as "English"
    And The parameter 'Information when recognizing a known PnP resource during start-up" is enabled in Setup -> System settings ->Task and Resource behaviou
    And The Instrument connected with the Balance
    And The connected balance is of category <category_fits> with the Instrument
    When The User Start up the Instrument
    Then The Terminal displays the Popup <popup-ID> on the screen
    And The User shall able to press 'Ok" on the Popup <popup-ID>
    Examples:
      | category_fits | popup-ID     |
      | fits          | Popup ID 108 |
      | wrong         | Popup ID 109 |

  # plug-in type ‘PnP USB Peripheral (=1) for Balances
  # Connecting when the same class & category of Balance connected already
  Scenario Outline: 45505_44085_Resource rules - Connecting Balances - Same class & category connected already
    Given The user is on the "Balance parameter" screen
    And The user is on "Balances" tab area
    And The language of Terminal set as "English"
    And The Instrument connected with the Balance category <category>
    When The User Start up the Instrument
    Then The Terminal displays the Popup <popup-ID> on the screen
    And The User shall able to press 'Ok" on the Popup <popup-ID>
    Examples:
    # TODO: Category "Mettler USB Juno" may included - TBD, Comment in SRD
      | category       | popup-ID     |
      | Mettler USB    | Popup ID 110 |
      | Mettler RS-232 | Popup ID 110 |

  # TODO: Resource rules: Editing the resource to verify the parameter "version" of the setup entry applies only on LCM


  # To verify the visibility of softkeys "Discard" and "Save"
  Scenario Outline: 44061_30327_"Balance parameter" screen - Unsaved changes - Softkeys verification
    Given The user is on the "Balance parameter" screen
    And The language of Terminal set as "English"
    And The user is on <tab_name> tab area
    When Parameters in <tab_name> tab area has new values
    Then The softkey "Cancel" is visible at position "1"
    And The softkey "Save" is visible at position "5"
    And The User cannot access the other tabs
    Examples:
      | tab_name |
      | Balances |
      | General  |


  Scenario Outline: 44061_30320(Discard)_"Balance parameter" screen - "Discard Changes" popup
    Given The user is on the "Balance parameter" screen
    And The language of Terminal set as "English"
    And The user is on <tab_name> tab area
    And Parameters in <tab_name> tab area has new values
    When The user presses the softkey "Discard"
    Then The Terminal displays the "popup ID 16" on the screen
    Examples:
      | tab_name |
      | Balances |
      | General  |

  Scenario: 44061_"Balance parameter" screen - "Discard Changes"_"No"
    Given The user is on the "popup ID 16"
    When The user presses "No" in "popup ID 16"
    Then The user is on the "Balance parameter" screen
    And The parameters are with updated values

  Scenario Outline: 44061_30320(Discard)_"Balance parameter" screen - "Discard Changes"- Yes
    Given The user is on the "Balance parameter" screen
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
      | tab_name |
      | Balances |
      | General  |

  Scenario Outline: 44061_30326(Save)_"Balance parameter" screen - "Save" softkey functionality
    Given The user is on the "Balance parameter" screen
    And The language of Terminal set as "English"
    And The user is on <tab_name> tab area
    And Parameters in <tab_name> tab area has new values
    And The User cannot access the other tabs
    When The user presses the softkey "Save"
    Then The Parameters on <tab_name> tab area is saved with updated values
    And The user is on <tab_name> tab area
    And The User can able to access the other tabs
    Examples:
      | tab_name |
      | Balances |
      | General  |


  # TODO: TBD_with Sandor, whether to include the verification - When starting a task and during the task, the connection of particular peripherals shall be checked (see [2] and [1])
  #  on requirement 46369 in SRD050 as part of SRD055 setup peripheral Balance Test case
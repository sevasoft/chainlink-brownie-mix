// SPDX-License-Identifier: MIT
pragma solidity >=0.8.7 <0.8.12;

import "@chainlink/contracts/src/v0.8/interfaces/KeeperCompatibleInterface.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Counters.sol";

contract Keeper is Ownable, KeeperCompatibleInterface {
    using Counters for Counters.Counter;

    Counters.Counter private _s_EmployeeCounter;

    struct Employee {
        address employee;
        uint256 paymentInterval;
        uint256 lastTimePaid;
        uint256 salary;
    }

    mapping(uint256 => Employee) public s_employees;

    address[] public employeesToPay;
    uint256 public employeesToPayLength;

    receive() external payable {}

    function addEmployee(address _employee, uint256 _paymentInterval, uint256 _salary)
        public
        onlyOwner
    {
        uint256 id = _s_EmployeeCounter.current();
        uint256 initialTimeStamp = block.timestamp;

        s_employees[id] = Employee(_employee, _paymentInterval, initialTimeStamp, _salary);
        _s_EmployeeCounter.increment();
    }

    function getEmployee(uint256 _id) public view returns (Employee memory) {
        return s_employees[_id];
    }

    function getTotalEmployees() public view returns (uint256) {
        return _s_EmployeeCounter.current();
    }

    function checkUpkeep(bytes calldata _checkData)
        external
        override 
        returns (bool upkeepNeeded, bytes memory performData)
    {
        uint256 totalEmployees = getTotalEmployees();
        address[] memory tempEmployeesToPay = new address[](totalEmployees);
        uint256 amountEmployeesToPay = 0;

        for (uint256 id = 0; id < totalEmployees; id++) {
            Employee memory employee = s_employees[id];

            if ((block.timestamp - employee.lastTimePaid) > employee.paymentInterval) {
                upkeepNeeded = true;
                tempEmployeesToPay[amountEmployeesToPay] = employee.employee;
                amountEmployeesToPay++;
            }
        }

        return (upkeepNeeded, abi.encode(tempEmployeesToPay, amountEmployeesToPay));
    }

    function performUpkeep(bytes calldata _performData)
        external
        override
    {
        (employeesToPay, employeesToPayLength) = abi.decode(_performData, (address[], uint256));
        payEmployee();
    }

    function payEmployee() public {
        for (uint256 id = 0; id < employeesToPayLength; id++) {
            Employee memory employee = s_employees[id];
            address payable employeeAddr = payable(employee.employee);
            uint256 salary = employee.salary;

            employeeAddr.transfer(salary);
        }
    }
}

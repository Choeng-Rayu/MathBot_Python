class BankAccount {
    // TODO
    final String _accountName;
    double _amount;
    BankAccount(this._accountName, [this._amount = 0]);

    double balance() => _amount;
    String withdraw(double amount) {
      if (amount > _amount || amount <= 0) return "The balance is not enough to withdraw";
      if (_amount == 0) return "Sorry you have no amount in your balance";
      _amount = _amount - amount;
      return "You have withdraw successfully!";
    }
    String credit(double amount) {
      if(amount <= 0 ) return "invalid amount, Please input again";
      _amount += amount;
      return "you have deposit successfully";
    }

}

class Bank {
    // TODO
  final String name;
  final BankAccount bankAccount;
  Bank(this.name, this.bankAccount);
  Bank.CreateAccount(BankAccount bankAccount, this.name) : bankAccount = bankAccount;
   

}
 
void main() {

  // Bank myBank = Bank(name: "CADT Bank");
  // BankAccount ronanAccount = myBank.createAccount(100, 'Ronan');

  // print(ronanAccount.balance); // Balance: $0
  // ronanAccount.credit(100);
  // print(ronanAccount.balance); // Balance: $100
  // ronanAccount.withdraw(50);
  // print(ronanAccount.balance); // Balance: $50

  // try {
  //   ronanAccount.withdraw(75); // This will throw an exception
  // } catch (e) {
  //   print(e); // Output: Insufficient balance for withdrawal!
  // }

  // try {
  //   myBank.createAccount(100, 'Honlgy'); // This will throw an exception
  // } catch (e) {
  //   print(e); // Output: Account with ID 100 already exists!
  // }
}

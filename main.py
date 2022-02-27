import sys
from getpass import getpass
from colorama import init, Fore, Back, Style
init()

SPECIAL_SYMBOLS = 4
NUMBERS = 3
CAPITAL_LETTERS = 2
LOWERCASE_LETTERS = 1
OTHER_CHARACTERS = 0

def repeatingCharacterTypeTest(password="") -> float:
    score = passLen = len(password)

    if not passLen:
        return .0

    lastCharacterType = -1

    for char in password:
        currentCharacterType = getCharacterType(char)
        if currentCharacterType == lastCharacterType:
            score -= 1
        lastCharacterType = currentCharacterType
    
    return score / len(password)


def getCharacterType(char="") -> int:
    alphabet = "abcdefghijklmnopqrstuvwxyz"

    if len(char) != 1:
        return -1
    if char in "!@#$%^&*()-=[]\\;',./_+{}|:\"<>?":
        return SPECIAL_SYMBOLS
    elif char in "1234567890":
        return NUMBERS
    elif char in alphabet.upper():
        return CAPITAL_LETTERS
    elif char in alphabet:
        return LOWERCASE_LETTERS

    return OTHER_CHARACTERS

def lenTest(password=""):
    passLen = len(password)
    if passLen:
        return 1 - ( 1 / ( (1/5) *  passLen + 1) )
    return 0

def _old_lenTest(password=""):
    plen = len(password)
    if plen <= 8:
        return 1/4
    elif plen <= 12:
        return 1/3
    elif plen <= 16:
        return 1/2
    return 1

def diversityTest(password=""):
    s = set()

    for c in password:
        s.add(c)

    return len(s) / len(password)

def _old_diversityTest(password=""):
    special_symbols = False
    numbers = False
    capital_letters = False
    lowercase_letters = False

    for char in password:
        charType = getCharacterType(char)

        if charType == SPECIAL_SYMBOLS:
            special_symbols = True
        elif charType == NUMBERS:
            numbers = True
        elif charType == CAPITAL_LETTERS:
            capital_letters = True
        else:
            lowercase_letters = True
    
    # w js coulda woosh [...].reduce((a, b) => a + b) without int(ing)
    total = int(special_symbols) + int(numbers) + int(capital_letters) + int(lowercase_letters)
    frac = total / 4
    return frac

def findNextOccurence(str, i) -> int:
    if len(str) == (i - 1):
        return -1;

    t = str[i];
    d = 0;
    f = False;
    for c in str[i+1:]:
        d += 1;
        if c == t:
            f = True;
            break
    return d if f else -1

# TODO: This thing is O(n^2) please code better :)
#! (might cancel)
def patternTest(str=""):
    repeats = 0;

    frc = ""
    lwr = False
    loc = -1;
    for i, x in enumerate(str[:-1]):
        d = findNextOccurence(str, i) if loc == -1 else loc
        nd = findNextOccurence(str, i + 1)

        # print(d, nd, x)

        if nd == d:
            if lwr:
                repeats += 0 if frc != x else 1
            else:
                repeats += 1
                frc == x
            lwr = True
            continue

        lwr = False

    return repeats

def printAssert(result: bool, str: str) -> None:
    color = Fore.RED
    out = "FAIL"
    if result:
        color = Fore.GREEN
        out = "PASS"
    
    print(f"{color}{out} - {str}{Fore.RESET}")
    pass

# i said screw oop but this seems convenient
# if this can b functional then sure ig c structures don't exist here 
# even tho this is POD
class Args:
    help = False
    noHide = False
    password = None

    def __init__(self, args):
        currIsValue = False

        for i, arg in enumerate(args):
            if currIsValue:
                currIsValue = False
                continue

            if arg == "-nh" or arg == "--no-hide":
                self.noHide = True
            elif arg == "-h" or arg == "--help":
                self.help = True
            elif arg == "-p" or arg == "--password":
                self.password = args[i + 1]
                currIsValue = True


def main(*args):
    sysArgs = Args(args[0])
 
    if sysArgs.help:
        print(f"{Back.GREEN}{Fore.BLACK}Password checker argument list:{Fore.RESET}{Back.RESET}\n")
        print(f"{Style.BRIGHT}[-p / --password] [VALUE]{Style.RESET_ALL} : Password argument")
        print(f"{Style.BRIGHT}[-nh / --no-hide]{Style.RESET_ALL} : Un-hides password input.")
        print(f"{Style.BRIGHT}[-h / --help]{Style.RESET_ALL} : Brings up this help menu")
        print(f"\nExample: {Style.BRIGHT}py main.py --password some_password{Style.RESET_ALL}\n")


        print(f"{Back.GREEN}{Fore.BLACK}Password checker test list:{Fore.RESET}{Back.RESET}")
        #! 1 ----------------------------------------------------------------------->
        print(f"\n1. {Style.BRIGHT}Repeating character test{Style.RESET_ALL}:")
        print("Tests for repeating character types as in\nthe more a character type repeats the less the score.")
        print("This also kills a few more birds with just one stone, it also tests character grouping and repetition.\n")
        lowPassword = "thisissomepassword"
        lowPasswordScore = repeatingCharacterTypeTest(lowPassword)
        print(f"An example of a low score password: {Fore.RED}{lowPassword}{Fore.RESET} (scored {round(lowPasswordScore * 100, 3)}%)")
        highPassword = "Th1s;s4gR3^tP4s$w0\\D"
        highPasswordScore = repeatingCharacterTypeTest(highPassword)
        print(f"An example of a better scored password: {Fore.GREEN}{highPassword}{Fore.RESET} (scored {round(highPasswordScore * 100, 3)}%)")
        #! 2 ----------------------------------------------------------------------->
        print(f"\n2. {Style.BRIGHT}Password length test{Style.RESET_ALL}:")
        print("Tests the (character) length of the password. The longer the better.")
        #! 3 ----------------------------------------------------------------------->
        print(f"\n3. {Style.BRIGHT}Password diversity test{Style.RESET_ALL}:")
        print("Tests character diversity of the password, the more unique characters there are the better.")
        return

    passStr = ""

    if sysArgs.password:
        passStr = sysArgs.password
    else:
        input_msg = ">> INPUT PASSWORD: "
        if sysArgs.noHide:
            passStr = input(input_msg)
        else:
            passStr = getpass(input_msg)
        
    c = 0
    t = 0
    
    repeatingCharacterTypeScore = repeatingCharacterTypeTest(passStr)
    rcts_threshold = 3/5
    rcts_result = repeatingCharacterTypeScore >= rcts_threshold
    printAssert(rcts_result, f"Repeating character test. [{round(repeatingCharacterTypeScore * 100, 3)}%]")
    c += repeatingCharacterTypeScore
    t += 1

    lenScore = lenTest(passStr)
    ls_threshold = 3/4
    ls_result = lenScore >= ls_threshold
    printAssert(ls_result, f"Password length test. [{round(lenScore * 100, 3)}%, length: {len(passStr)}]")
    c += lenScore
    t += 1

    diversityScore = diversityTest(passStr)
    d_threshhold = 1/2
    d_result = diversityScore >= d_threshhold
    printAssert(d_result, f"Diversity test. [{round(diversityScore * 100, 3)}%]")
    c += diversityScore
    t += 1

    avg = round(c/t*100, 3)
    print(f"\n{Style.BRIGHT}Total: {round(c, 3)}/{t} passed, avg {avg}%{Style.RESET_ALL}")

    color = None
    res = None
    if avg < 50:
        color = Fore.RED
        res = "Weak"
    elif avg < 75:
        color = Fore.YELLOW
        res = "Average"
    else:
        color = Fore.GREEN
        res = "Strong"
    
    print(f"{Style.BRIGHT}Result: {color}{res}{Fore.RESET}.{Style.RESET_ALL}")
    # print(Style.BRIGHT + "Result: " + color + res + Fore.RESET + "." + Style.RESET_ALL)

if __name__ == "__main__":
    main(sys.argv[1:])

# TOPIC 1.1 Why Programming? Why Java?  

# Required Course Content  

# ENDURING UNDERSTANDING  

# MOD-1  

Some objects or concepts are so frequently represented that programmers can draw upon existing code that has already been tested, enabling them to write solutions more quickly and with a greater degree of confidence.  

# LEARNING OBJECTIVE ESSENTIAL KNOWLEDGE  

# MOD-1.A  

MOD-1.A.1  

Call System class methods to generate output to the console.  

System.out.print and System.out. println display information on the computer monitor.  

MOD-1.A.2  

System.out.println moves the cursor to a new line after the information has been displayed, while System.out.print does not.  

# ENDURING UNDERSTANDING  

# VAR-1  

To find specific solutions to generalizable problems, programmers include variables in their code so that the same algorithm runs using different input values.  

# LEARNING OBJECTIVE ESSENTIAL KNOWLEDGE  

VAR-1.A  

VAR-1.A.1  

Create string literals.  

A string literal is enclosed in double quotes.  

# SUGGESTED SKILLS  

# TOPIC 1.2 Variables and Data Types  

Determine an appropriate program design to solve a problem or accomplish a task.  

Determine code that would be used to complete code segments.  

# Required Course Content  

![](images/8ea3f612520c413463797ab03fad52f3c1995be08cd306cf180c2fb95c5f102d.jpg)  

# AVAILABLE RESOURCE  

§ Runestone Academy: AP CSA—Java Review: 3—Variables  

# ENDURING UNDERSTANDING  

# VAR-1  

To find specific solutions to generalizable problems, programmers include variables in their code so that the same algorithm runs using different input values.  

# LEARNING OBJECTIVE ESSENTIAL KNOWLEDGE  

# VAR-1.B  

# VAR-1.B.1  

Identify the most appropriate data type category for a particular specification.  

A type is a set of values (a domain) and a set of operations on them.  

# VAR-1.B.2  

Data types can be categorized as either primitive or reference.  

# VAR-1.B.3  

The primitive data types used in this course define the set of operations for numbers and Boolean values.  

# VAR-1.C  

# VAR-1.C.1  

Declare variables of the correct types to represent primitive data.  

The three primitive data types used in this course are int, double, and boolean.  

# VAR-1.C.2  

Each variable has associated memory that is used to hold its value.  

# VAR-1.C.3  

The memory associated with a variable of a primitive type holds an actual primitive value.  

# VAR-1.C.4  

When a variable is declared final, its value cannot be changed once it is initialized.  

# SUGGESTED SKILLS  

Determine code that would be used to complete code segments.  

# 2.A  

Apply the meaning of specific operators.  

# TOPIC 1.3 Expressions and Assignment Statements  

# AVAILABLE RESOURCES  

· Runestone Academy: AP CSA—Java Review: 3.5—Operators ·Problets: Arithmetic Expressions in Java  

# Required Course Content  

# ENDURING UNDERSTANDING  

# CON-1  

The way variables and operators are sequenced and combined in an expression determines the computed result.  

# LEARNING OBJECTIVE ESSENTIAL KNOWLEDGE  

# CON-1.A  

Evaluate arithmetic expressions in a program code.  

# CON-1.A.1  

A literal is the source code representation of a fixed value.  

# CON-1.A.2  

Arithmetic expressions include expressions of type int and double.  

# CON-1.A.3  

The arithmetic operators consist of $+,-,\star,/$ , and $\%$ .  

# CON-1.A.4  

An arithmetic operation that uses two int values will evaluate to an int value.  

# CON-1.A.5  

An arithmetic operation that uses a double value will evaluate to a double value.  

# CON-1.A.6  

Operators can be used to construct compound expressions.  

# CON-1.A.7  

During evaluation, operands are associated with operators according to operator precedence to determine how they are grouped.  

# CON-1.A.8  

An attempt to divide an integer by zero will result in an ArithmeticException to occur.  

# Primitive Types  

# LEARNING OBJECTIVE ESSENTIAL KNOWLEDGE  

# CON-1.B  

# CON-1.B.1  

Evaluate what is stored in a variable as a result of an expression with an assignment statement.  

The assignment operator $(=)$ allows a program to initialize or change the value stored in a variable. The value of the expression on the right is stored in the variable on the left.  

# CON-1.B.2  

During execution, expressions are evaluated to produce a single value.  

# CON-1.B.3  

The value of an expression has a type based on the evaluation of the expression.  

# SUGGESTED SKILLS  

Determine the result or output based on statement execution order in a code segment without method calls (other than output).  

# 5.A  

Describe the behavior of a given segment of program code.  

![](images/e7e8927a0c5794041e9ec4135bc14b88cc7e6ae66a820bc0e3aeeee2f39b0e7a.jpg)  

# AVAILABLE RESOURCE  

§ Runestone Academy: AP CSA—Java Review: 3.5—Operators  

# TOPIC 1.4 Compound Assignment Operators  

# Required Course Content  

# ENDURING UNDERSTANDING  

# CON-1  

The way variables and operators are sequenced and combined in an expression determines the computed result.  

# LEARNING OBJECTIVE ESSENTIAL KNOWLEDGE  

CON-1.B  

CON-1.B.4  

Evaluate what is stored in a variable as a result of an expression with an assignment statement.  

Compound assignment operators $(+=,-=,\star=,$ $\slash=,\mathtt{s}=\mathtt{}$ can be used in place of the assignment operator.  

# CON-1.B.5  

The increment operator $(++)$ and decrement operator $(--)$ are used to add 1 or subtract 1 from the stored value of a variable or an array element. The new value is assigned to the variable or array element.  

# EXCLUSION STATEMENT-(EK CON-1.B.5):  

The use of increment and decrement operators in prefix form (i.e., $++{\bf x})$ and inside other expressions (i.e., $\arctan(\mathbf{x}+\mathbf{+}])$ is outside the scope of this course and the AP Exam.  

# TOPIC 1.5 Casting and Ranges of Variables  

# SUGGESTED SKILLS  

Determine the result or output based on statement execution order in a code segment without method calls (other than output).  

Explain why a code segment will not compile or work as intended.  

# Required Course Content  

# ENDURING UNDERSTANDING  

# AVAILABLE RESOURCE  

§ Runestone Academy: AP CSA—Java Review: 3.6—Casting  

# CON-1  

The way variables and operators are sequenced and combined in an expression determines the computed result.  

# LEARNING OBJECTIVE ESSENTIAL KNOWLEDGE  

# CON-1.C  

# CON-1.C.1  

Evaluate arithmetic expressions that use casting.  

The casting operators (int) and (double) can be used to create a temporary value converted to a different data type.  

# CON-1.C.2  

Casting a double value to an int causes the digits to the right of the decimal point to be truncated.  

# CON-1.C.3  

Some programming code causes int values to be automatically cast (widened) to double values.  

# CON-1.C.4  

Values of type double can be rounded to the nearest integer by (int) $({\bf x}+0.5)$ or (int) $({\bf x}-0.5)$ for negative numbers.  

# CON-1.C.5  

Integer values in Java are represented by values of type int, which are stored using a finite amount (4 bytes) of memory. Therefore, an int value must be in the range from Integer.MIN_VALUE to Integer.MAX VALUE inclusive.  

# CON-1.C.6  

If an expression would evaluate to an int value outside of the allowed range, an integer overflow occurs. This could result in an incorrect value within the allowed range.  

# AP COMPUTER SCIENCE A  

# UNIT 2 Using Objects  

Remember to go to AP Classroom to assign students the online Personal Progress Check for this unit.  

Whether assigned as homework or completed in class, the Personal Progress Check provides each student with immediate feedback related to this unit’s topics and skills.  

# Personal Progress Check 2  

Multiple-choice: \~25 questions Free-response: 1 question  

$\cdot$ Methods and Control Structures: partial  

![](images/2c00483827f003cc3310826cce7b29d1fff63aaa0900add45edff65614c1eb90.jpg)  

<html><body><table><tr><td>5-7.5% APEXAMWEIGHTING</td><td>~13-15 CLASSPERIODS</td></tr></table></body></html>  

# Using Objects  

# Developing Understanding  

# BIG IDEA 1 Modularity MOD  

§ How can we simulate election results using existing program code?  

# BIG IDEA 2 Variables  VAR  

§ How are appropriate variables chosen to represent a remote control?  

BIG IDEA 3 Control  CON · How do the games we play simulate randomness?  

In the first unit, students used primitive types to represent real-world data and determined how to use them in arithmetic expressions to solve problems. This unit introduces a new type of data: reference data. Reference data allows real-world objects to be represented in varying degrees specific to a programmer’s purpose. This unit builds on students’ ability to write expressions by introducing them to Math class methods to write expressions for generating random numbers and other more complex operations. In addition, strings and the existing methods within the String class are an important topic within this unit. Knowing how to declare variables or call methods on objects is necessary throughout the course but will be very important in Units 5 and 9 when teaching students how to write their own classes and about inheritance relationships.  

# Building Computational Thinking Practices  

# 1.B 1.C 3.A  

The study of computer science involves implementing the design or specification for a program. This is the fun and rewarding part of computer science, because it involves putting a plan into practice to create a runnable program. In addition to developing their own programs, students should practice completing partially written program code to fulfill a specification. This builds their confidence and provides them opportunities to be successful during these early stages of learning.  

Programmers often rely on existing program code to build new programs. Using existing code saves time, because it has already been tested. By using the String class, students will learn how to interact with and utilize any existing Java class to create objects and call methods.  

# Preparing for the AP Exam  

During the free-response portion of the exam, students will be required to call methods of classes that they haven’t been exposed to prior to the exam. Students should get plenty of practice identifying the proper parameters to use when calling methods of classes that are provided to them.  

Often, students struggle with free-response questions that require them to work with the String class. Using the Java Quick Reference (p. 219) regularly during class will help students become more familiar with this resource prior to the exam. Paying close attention to the method descriptions will ensure that students use the correct type and order of parameters when calling String methods.  

Practice close reading techniques with students prior to the exam, such as underlining keywords, return types, and parameters. Students have approximately 20 minutes to read, process, and answer each of the four free-response questions. These close reading techniques are valuable in helping students process the questions quickly without inadvertently missing key information.  

![](images/1f64904233254572479b5d78df063fba83e5c373295b2a58a90a02bb412a1e57.jpg)  

# Using Objects  

# UNITATAGLANCE  

<html><body><table><tr><td>E5</td><td>Topic</td><td>Suggested Skills</td><td>CLASS PERIODS</td></tr><tr><td>MOD-1</td><td>2.1 Objects: Instances of Classes</td><td>5.ADescribe the behavior of a given segment of program code.</td><td></td></tr><tr><td rowspan="3"></td><td rowspan="3">2.2 Creating and Storing Objects (Instantiation)</td><td>1.C Determine code that would be used to interact with completed program code.</td><td></td></tr><tr><td>3.A Write program code to create objects of a class and call methods.</td><td></td></tr><tr><td>1.cDetermine code that would be used to interact with completed program code.</td><td></td></tr><tr><td rowspan="5">MOD-1</td><td>Method 2.4 Calling a Void</td><td>3.A Write program code to create objects of a class and call methods.</td><td></td></tr><tr><td rowspan="3">Method with Parameters 2.5 Calling a Non-void</td><td>2.cDetermine theresultoroutputbasedonthestatement execution orderin a code segmentcontaining method calls.</td><td></td></tr><tr><td>3.AWrite program code to create objects of a class and call methods.</td><td></td></tr><tr><td>1.C Determine code that would be used to interact with completed program code.</td><td></td></tr><tr><td>Method</td><td>3.A Write program code to create objects of a class and call methods.</td><td></td></tr><tr><td rowspan="4">VAR-1</td><td>2.6 String Objects: Concatenation, Literals, and More</td><td>2.AApply the meaning of specific operators.</td><td></td></tr><tr><td>2.7 String Methods</td><td>2.cDeterminetheresultoroutputbased onthe statement execution orderina code segmentcontaining method calls. 3.A Write program code to create objects of a class and call methods.</td><td></td></tr><tr><td>2.8 Wrapper Classes: Integer and Double</td><td>2.cDetermine theresult or output based on the statement execution order in a code segment containing method calls.</td><td></td></tr><tr><td>2.9 Using the Math Class</td><td>1.BDetermine code that would be used to complete</td><td></td></tr><tr><td>MOD N COI</td><td></td><td>code segments. 3.A Writeprogramcodetocreateobjectsofa class and callmethods.</td><td></td></tr></table></body></html>  

# SAMPLE INSTRUCTIONAL ACTIVITIES  

The sample activities on this page are optional and are offered to provide possible ways to incorporate instructional approaches into the classroom. They were developed in partnership with teachers from the AP community to share ways that they approach teaching some of the topics in this unit. Please refer to the Instructional Approaches section beginning on p. 159 for more examples of activities and strategies.  

<html><body><table><tr><td>Activity</td><td>Topic</td><td>Sample Activity</td></tr><tr><td rowspan="3">1</td><td>2.1</td><td>Usingmanipulatives Whenintroducingstudentstotheideaofcreatingobjects,youcanuseacookiecutter</td></tr><tr><td></td><td>andmodelingclayordough,withthecutterrepresentingtheclassandthecutdough representing the objects.Foreachobjectcut,write theinstantiation.Askstudents</td></tr><tr><td></td><td>to describe what the code is doing and how the different parameter values (e.g.. thickness,color)changetheobjectthatwascreated.</td></tr><tr><td>2</td><td>2.2</td><td>Marking the text Providestudentswithseveral statements thatdefine avariableandcreateanobject operatorand thenewkeyword.Then,have students underline thevariable type andtheconstructor.Lastly,havethemdrawarectanglearoundthelistofactual</td></tr><tr><td></td><td>2.9</td><td>parameters being passed to the constructor.Using these marked-up statements, ask studentstocreateseveralnewvariablesandobjects.</td></tr><tr><td>3</td><td></td><td>Think-pair-share Providestudentswithseveral codesegments,eachwithamissingexpressionthat wouldcontainacalltoamethodintheMathclass,andadescriptionoftheintended</td></tr></table></body></html>  

# Unit Planning Notes  

Use the space below to plan your approach to the unit. Consider how you want to pace your course and where you will incorporate writing and analyzing program code.  

# SUGGESTED SKILL  

Describe the behavior of a given segment of program code.  

# TOPIC 2.1 Objects: Instances of Classes  

# AVAILABLE RESOURCE  

· Runestone Academy: AP CSA—Java Review: 2.2—What is a Class and an Object?  

# Required Course Content  

# ENDURING UNDERSTANDING  

# MOD-1  

Some objects or concepts are so frequently represented that programmers can draw upon existing code that has already been tested, enabling them to write solutions more quickly and with a greater degree of confidence.  

# LEARNING OBJECTIVE ESSENTIAL KNOWLEDGE  

# MOD-1.B  

# MOD-1.B.1  

Explain the relationship between a class and an object.  

An object is a specific instance of a class with defined attributes.  

# MOD-1.B.2  

A class is the formal implementation, or blueprint, of the attributes and behaviors of an object.  

# TOPIC 2.2 Creating and Storing Objects (Instantiation)  

SUGGESTED SKILLS  

Determine code that would be used to interact with completed program code.  

Write program code to create objects of a class and call methods.  

# Required Course Content  

# ENDURING UNDERSTANDING  

# MOD-1  

Some objects or concepts are so frequently represented that programmers can draw upon existing code that has already been tested, enabling them to write solutions more quickly and with a greater degree of confidence.  

# LEARNING OBJECTIVE ESSENTIAL KNOWLEDGE  

# MOD-1.C  

# MOD-1.C.1  

Identify, using its signature, the correct constructor being called.  

A signature consists of the constructor name and the parameter list.  

# MOD-1.C.2  

The parameter list, in the header of a constructor, lists the types of the values that are passed and their variable names. These are often referred to as formal parameters.  

# MOD-1.C.3  

A parameter is a value that is passed into a constructor. These are often referred to as actual parameters.  

# MOD-1.C.4  

Constructors are said to be overloaded when there are multiple constructors with the same name but a different signature.  

# MOD-1.C.5  

The actual parameters passed to a constructor must be compatible with the types identified in the formal parameter list.  

# MOD-1.C.6  

Parameters are passed using call by value. Call by value initializes the formal parameters with copies of the actual parameters.  

# Using Objects  

# LEARNING OBJECTIVE ESSENTIAL KNOWLEDGE  

# MOD-1.D  

For creating objects:  

a. Create objects by calling constructors without parameters.   
b. Create objects by calling constructors with parameters.  

# MOD-1.D.1  

Every object is created using the keyword new followed by a call to one of the class’s constructors.  

# MOD-1.D.2  

A class contains constructors that are invoked to create objects. They have the same name as the class.  

# MOD-1.D.3  

Existing classes and class libraries can be utilized as appropriate to create objects.  

# MOD-1.D.4  

Parameters allow values to be passed to the constructor to establish the initial state of the object.  

# ENDURING UNDERSTANDING  

# VAR-1  

To find specific solutions to generalizable problems, programmers include variables in their code so that the same algorithm runs using different input values.  

# ESSENTIAL KNOWLEDGE  

# VAR-1.D  

Define variables of the correct types to represent reference data.  

# VAR-1.D.1  

The keyword null is a special value used to indicate that a reference is not associated with any object.  

# VAR-1.D.2  

The memory associated with a variable of a reference type holds an object reference value or, if there is no object, null. This value is the memory address of the referenced object.  

# TOPIC 2.3 Calling a Void Method  

SUGGESTED SKILLS  

Determine code that would be used to interact with completed program code.  

Write program code to create objects of a class and call methods.  

![](images/36bde30d3ed6ab43f5c1d7a94a5408435097b47b17d4dd71ae507ef975c88881.jpg)  

# Required Course Content  

# AVAILABLE RESOURCE  

§ Classroom Resources > GridWorld Case Study: Part I  

# ENDURING UNDERSTANDING  

# MOD-1  

Some objects or concepts are so frequently represented that programmers can draw upon existing code that has already been tested, enabling them to write solutions more quickly and with a greater degree of confidence.  

# LEARNING OBJECTIVE ESSENTIAL KNOWLEDGE  

# MOD-1.E  

# MOD-1.E.1  

Call non-static void methods without parameters.  

An object’s behavior refers to what the object can do (or what can be done to it) and is defined by methods.  

# MOD-1.E.2  

Procedural abstraction allows a programmer to use a method by knowing what the method does even if they do not know how the method was written.  

# MOD-1.E.3  

A method signature for a method without parameters consists of the method name and an empty parameter list.  

# MOD-1.E.4  

A method or constructor call interrupts the sequential execution of statements, causing the program to first execute the statements in the method or constructor before continuing. Once the last statement in the method or constructor has executed or a return statement is executed, flow of control is returned to the point immediately following where the method or constructor was called.  

# Using Objects  

# LEARNING OBJECTIVE ESSENTIAL KNOWLEDGE  

MOD-1.E  

# MOD-1.E.5  

Call non-static void methods without parameters.  

Non-static methods are called through objects of the class.  

# MOD-1.E.6  

The dot operator is used along with the object name to call non-static methods.  

# MOD-1.E.7  

Void methods do not have return values and are therefore not called as part of an expression.  

# MOD-1.E.8  

Using a null reference to call a method or access an instance variable causes a NullPointerException to be thrown.  

# TOPIC 2.4 Calling a Void Method with Parameters  

# SUGGESTED SKILLS  

Determine the result or output based on the statement execution order in a code segment containing method calls.  

Write program code to create objects of a class and call methods.  

# Required Course Content  

# ENDURING UNDERSTANDING  

# AVAILABLE RESOURCE  

# MOD-1  

§ Practice-It!: BJP4 Chapter 3: Parameters and Objects—SelfCheck 3.2–3.9  

Some objects or concepts are so frequently represented that programmers can draw upon existing code that has already been tested, enabling them to write solutions more quickly and with a greater degree of confidence.  

# LEARNING OBJECTIVE ESSENTIAL KNOWLEDGE  

# MOD-1.F  

# MOD-1.F.1  

Call non-static void methods with parameters.  

A method signature for a method with parameters consists of the method name and the ordered list of parameter types.  

# MOD-1.F.2  

Values provided in the parameter list need to correspond to the order and type in the method signature.  

# MOD-1.F.3  

Methods are said to be overloaded when there are multiple methods with the same name but a different signature.  

# SUGGESTED SKILLS  

Determine code that would be used to interact with completed program code.  

Write program code to create objects of a class and call methods.  

![](images/20e71a7f417e31ee92b4d249b8b10ac4df2be58dd370f36056c6baa18f82cba5.jpg)  

# AVAILABLE RESOURCES  

The Exam $>$ 2018 AP Computer Science A Exam Free‐Response Question #1 (Frog Simulation)  

# TOPIC 2.5 Calling a Non-void Method  

# Required Course Content  

# ENDURING UNDERSTANDING  

# MOD-1  

Some objects or concepts are so frequently represented that programmers can draw upon existing code that has already been tested, enabling them to write solutions more quickly and with a greater degree of confidence.  

# LEARNING OBJECTIVE ESSENTIAL KNOWLEDGE  

# MOD-1.G  

# MOD-1.G.1  

Call non-static non-void methods with or without parameters.  

Non-void methods return a value that is the same type as the return type in the signature. To use the return value when calling a non-void method, it must be stored in a variable or used as part of an expression.  

# TOPIC 2.6  

# String Objects: Concatenation, Literals, and More  

SUGGESTED SKILL  

Apply the meaning of specific operators.  

Required Course Content  

# AVAILABLE RESOURCES  

§ Runestone Academy: AP CSA—Java Review:   
4—Strings   
Practice-It!:BJP4 Chapter 3: Parameters and Objects—SelfCheck 3.18  

# ENDURING UNDERSTANDING  

# VAR-1  

To find specific solutions to generalizable problems, programmers include variables in their code so that the same algorithm runs using different input values.  

# LEARNING OBJECTIVE ESSENTIAL KNOWLEDGE  

# VAR-1.E  

# VAR-1.E.1  

For String class: a. Create String objects. b. Call String methods.  

String objects can be created by using string literals or by calling the String class constructor.  

# VAR-1.E.2  

String objects are immutable, meaning that String methods do not change the String object.  

# VAR-1.E.3  

String objects can be concatenated using the $+$ or $+=$ operator, resulting in a new String object.  

# VAR-1.E.4  

Primitive values can be concatenated with a String object. This causes implicit conversion of the values to String objects.  

# VAR-1.E.5  

Escape sequences start with a \ and have a special meaning in Java. Escape sequences used in this course include \”, \\, and \n.  

# SUGGESTED SKILLS  

Determine the result or output based on the statement execution order in a code segment containing method calls.  

Write program code to create objects of a class and call methods.  

![](images/3fbccda764768fd39c05bd5f812cc5b7571d407afd63fa9bfea3e6e2fbc2c78c.jpg)  

# AVAILABLE RESOURCES  

· Java Quick Reference (see Appendix)   
Runestone Academy: AP CSA—Java Review: 4.3—String Methods on the Exam   
§ CodingBat Java: String‐1   
§ Practice‐It!: BJP4 Chapter 3: Parameters and Objects—Self‐ Check 3.19 and 3.20  

# Using Objects  

# TOPIC 2.7 String Methods  

# Required Course Content  

# ENDURING UNDERSTANDING  

# VAR-1  

To find specific solutions to generalizable problems, programmers include variables in their code so that the same algorithm runs using different input values.  

# LEARNING OBJECTIVE ESSENTIAL KNOWLEDGE  

# VAR-1.E  

For String class: a. Create String objects. b. Call String methods.  

# VAR-1.E.6  

Application program interfaces (APIs) and libraries simplify complex programming tasks.  

# VAR-1.E.7  

Documentation for APIs and libraries are essential to understanding the attributes and behaviors of an object of a class.  

# VAR-1.E.8  

Classes in the APIs and libraries are grouped into packages.  

# VAR-1.E.9  

The String class is part of the java.lang package. Classes in the java.lang package are available by default.  

# VAR-1.E.10  

A String object has index values from 0 to length - 1. Attempting to access indices outside this range will result in an IndexOutOfBoundsException.  

# VAR-1.E.11  

A String object can be concatenated with an object reference, which implicitly calls the referenced object’s toString method.  

# Using Objects  

# LEARNING OBJECTIVE  

# ESSENTIAL KNOWLEDGE  

VAR-1.E  

For String class: a. Create String objects. b. Call String methods.  

# VAR-1.E.12  

The following String methods and constructors—including what they do and when they are used—are part of the Java Quick Reference:  

§ String(String str) — Constructs a new String object that represents the same sequence of characters as str   
int length()— Returns the number of characters in a String object   
§ String substring(int from, int to)—Returns the substring beginning at index from and ending at index to − 1 String substring(int from) — Returns substring(from, length())   
int indexOf(String str) — Returns the index of the first occurrence of str; returns -1 if not found   
boolean equals(String other) — Returns true if this is equal to other; returns false otherwise int compareTo(String other) — Returns a value $<0$ if this is less than other; returns zero if this is equal to other; returns a value $>0$ if this is greater than other  

# VAR-1.E.13  

A string identical to the single element substring at position index can be created by calling substring(index, index $^+\beth$ ).  

# SUGGESTED SKILL  

Determine the result or output based on the statement execution order in a code segment containing method calls.  

# TOPIC 2.8 Wrapper Classes: Integer and Double  

# AVAILABLE RESOURCE  

· Java Quick Reference (see Appendix)  

# Required Course Content  

# ENDURING UNDERSTANDING  

# VAR-1  

To find specific solutions to generalizable problems, programmers include variables in their code so that the same algorithm runs using different input values.  

# LEARNING OBJECTIVE ESSENTIAL KNOWLEDGE  

# VAR-1.F  

# VAR-1.F.1  

For wrapper classes:  

a. Create Integer objects.   
b. Call Integer methods.   
c. Create Double objects.   
d. Call Double methods.  

The Integer class and Double class are part of the java.lang package.  

# VAR-1.F.2  

The following Integer methods and constructors—including what they do and when they are used—are part of the Java Quick Reference:  

Integer(int value) — Constructs a new Integer object that represents the specified int value   
Integer.MIN_VALUE—The minimum value represented by an int or Integer Integer .MAx_VALUE—The maximum value represented by an int or Integer int intValue()— Returns the value of this Integer as an int  

# Using Objects  

# LEARNING OBJECTIVE ESSENTIAL KNOWLEDGE  

VAR-1.E  

# VAR-1.F.3  

For wrapper classes:  

a. Create Integer objects.   
b. Call Integer methods.   
c. Create Double objects.   
d. Call Double methods.  

The following Double methods and constructors—including what they do and when they are used—are part of the Java Quick Reference:  

§ Double(double value) — Constructs a new Double object that represents the specified double value double doubleValue()—Returns the value of this Double as a double  

# VAR-1.F.4  

Autoboxing is the automatic conversion that the Java compiler makes between primitive types and their corresponding object wrapper classes. This includes converting an int to an Integer and a double to a Double.  

# VAR-1.F.5  

The Java compiler applies autoboxing when a primitive value is:  

· Passed as a parameter to a method that expects an object of the corresponding wrapper class.   
§ Assigned to a variable of the corresponding wrapper class.  

# VAR-1.F.6  

Unboxing is the automatic conversion that the Java compiler makes from the wrapper class to the primitive type. This includes converting an Integer to an int and a Double to a double.  

# VAR-1.F.7  

The Java compiler applies unboxing when a wrapper class object is:  

§ Passed as a parameter to a method that expects a value of the corresponding primitive type.   
§ Assigned to a variable of the corresponding primitive type.  

# SUGGESTED SKILLS  

Determine code that would be used to complete code segments.  

Write program code to create objects of a class and call methods.  

![](images/af5059513df8dc8bb3a821a07eee69c59563da3b5af55eedec72178afa973675.jpg)  

# TOPIC 2.9 Using the Math Class  

# AVAILABLE RESOURCES  

· Java Quick Reference (see Appendix) § Practice-It!: BJP4 Chapter 3: Parameters and Objects— Exercises 3.7 and 3.8  

# Using Objects  

# Required Course Content  

# ENDURING UNDERSTANDING  

# MOD-1  

Some objects or concepts are so frequently represented that programmers can draw upon existing code that has already been tested, enabling them to write solutions more quickly and with a greater degree of confidence.  

# LEARNING OBJECTIVE ESSENTIAL KNOWLEDGE  

# MOD-1.H  

# MOD-1.H.1  

Call static methods.  

Static methods are called using the dot operator along with the class name unless they are defined in the enclosing class.  

# ENDURING UNDERSTANDING  

# CON-1  

The way variables and operators are sequenced and combined in an expression determines the computed result.  

# LEARNING OBJECTIVE ESSENTIAL KNOWLEDGE  

# CON-1.D  

Evaluate expressions that use the Math class methods.  

CON-1.D.1  

The Math class is part of the java.lang package.  

# CON-1.D.2  

The Math class contains only static methods.  

# Using Objects  

# LEARNING OBJECTIVE ESSENTIAL KNOWLEDGE  

# CON-1.D  

# CON-1.D.3  

Evaluate expressions that use the Math class methods.  

The following static Math methods—including what they do and when they are used—are part of the Java Quick Reference:  

§ int abs(int x) — Returns the absolute value of an int value double abs(double x) — Returns the absolute value of a double value double pow(double base, double exponent) — Returns the value of the first parameter raised to the power of the second parameter § double sqrt(double x) — Returns the positive square root of a double value double random() — Returns a double value greater than or equal to 0.0 and less than 1.0  

# CON-1.D.4  

The values returned from Math.random can be manipulated to produce a random int or double in a defined range.  

# AP COMPUTER SCIENCE A  

# UNIT 3  

# Boolean Expressions and if Statements  

Remember to go to AP Classroom to assign students the online Personal Progress Check for this unit.  

Whether assigned as homework or completed in class, the Personal Progress Check provides each student with immediate feedback related to this unit’s topics and skills.  

# Personal Progress Check 3  

# Multiple-choice: \~20 questions Free-response: 2 questions  

$\cdot$ Methods and Control Structures Methods and Control Structures: partial  

# Boolean Expressions and if Statements  

# Developing Understanding  

# BIG IDEA 1  

# Control CON  

■ How can you use different conditional statements to write a pick-your-own-path interactive story? § Why is selection a necessary part of programming languages?  

Algorithms are composed of three building blocks: sequencing, selection, and iteration. This unit focuses on selection, which is represented in a program by using conditional statements. Conditional statements give the program the ability to decide and respond appropriately and are a critical aspect of any nontrivial computer program. In addition to learning the syntax and proper use of conditional statements, students will build on the introduction of Boolean variables by writing Boolean expressions with relational and logical operators.  

The third building block of all algorithms is iteration, which you will cover in Unit 4. Selection and iteration work together to solve problems.  

# Building Computational Thinking Practices  

# 2.B 3.C 4.A 4.C  

Selection allows programmers to incorporate choice into their programs: to create games that react to interactions of the user, to develop simulations that are more real world by allowing for variability, or to discover new knowledge in a sea of information by filtering out irrelevant data. Students should be able to write program code that uses conditional statements for selection. Have students write their program code on paper and trace it with different sample inputs before writing code on the computer.  

# Preparing for the AP Exam  

Programmers need to make design decisions when creating programs that determine how a program specification will be implemented. Typically, there are many ways in which statements can be written to yield the same result, and this final determination is dictated by the programmer. Exposing students to many different code segments that yield equivalent results allows them to be more confident in their solution and helps expose them to new ways of solving the problem that may be better than their current solution.  

The study of computer science involves the analysis of program code. On the multiplechoice section of the exam, students will be asked to determine the result of a given program code segment based on specific input and on the behavior of program code in general. Students should be able to determine the result of program code that uses conditional statements and nested conditional statements to represent nonlinear processes in a program.  

Often, students will write program code that mishandles one of the given conditions. The ability to trace program code can be valuable when testing programs to ensure that all conditions are met. Testing for the different expected behaviors of conditional statements is a critical part of program development and is useful when writing program code or analyzing given code segments. Students should develop sample test cases to illustrate each unique behavior to aid in finding errors and validating results.  

![](images/c85ce3ce9ff4acafb934c27386f52b91e17911293c55a31b1c75cdf5351cc794.jpg)  

# Boolean Expressions and if Statements  

<html><body><table><tr><td colspan="4"></td></tr><tr><td colspan="4"></td></tr><tr><td>Enduring</td><td>Topic 3.1 Boolean Expressions</td><td>Suggested Skills 2.A  Apply the meaning of specific operators.</td><td>~11-13 CLASS PERIODS</td></tr><tr><td>CON-</td><td>3.2 if Statements and</td><td>2.BDetermine the result or output based on</td><td></td></tr><tr><td rowspan="5">CON-2</td><td>Control Flow</td><td>statementexecutionorderina codesegment without method calls (other than output). 3.cWrite program code to satisfy method specifications using expressions, conditional statements,and iterative statements.</td><td></td></tr><tr><td>3.3 if-else Statements</td><td>3.cWrite program code to satisfy method specifications using expressions, conditional</td><td></td></tr><tr><td></td><td>statements,and iterative statements. 4.A Usetest-casestofinderrorsor validate results.</td><td></td></tr><tr><td>3.4 else if Statements</td><td>3.C Write program code to satisfy method specifications using expressions, conditional</td><td></td></tr><tr><td>4.C</td><td>statements,and iterative statements. Determine if two or more code segments yield equivalentresults.</td><td></td></tr><tr><td>CON-1, CON-2</td><td>3.5 Compound Boolean Expressions</td><td>2.BDetermine theresultor outputbased on statementexecutionorderina codesegment without method calls (other than output). 3.CWrite program code to satisfy method specifications using expressions, conditional</td><td></td></tr><tr><td rowspan="2">CON-1</td><td>3.6 Equivalent Boolean Expressions</td><td>statements,and iterative statements. 4.C Determine if two or more code segments yield equivalentresults.</td><td></td></tr><tr><td>3.7 Comparing Objects 3.A  Write program code to create objects of a</td><td>2.cDetermine theresultor outputbased on the statementexecutionorderina codesegment containing method calls.</td><td></td></tr></table></body></html>  

# SAMPLE INSTRUCTIONAL ACTIVITIES  

The sample activities on this page are optional and are offered to provide possible ways to incorporate instructional approaches into the classroom. They were developed in partnership with teachers from the AP community to share ways that they approach teaching some of the topics in this unit. Please refer to the Instructional Approaches section beginning on p. 159 for more examples of activities and strategies.  

<html><body><table><tr><td>Activity</td><td>Topic</td><td>Sample Activity</td></tr><tr><td>1</td><td>3.3</td><td>Code tracing Providestudentswithseveral codesegmentsthatcontainconditionalstatements.</td></tr><tr><td></td><td></td><td>Have students trace various sample inputs, keeping track of the statements that get executed and the orderinwhich they areexecuted.Thiscanhelpstudentsfind errors andvalidateresults.</td></tr><tr><td>2</td><td>3.2-3.5</td><td>Pair programming Havestudentsworkwithapartnertocreatea"guesschecker"thatcould beused as</td></tr><tr><td></td><td></td><td>partofalargergame.Studentscomparefourgivendigitstoapreexistingfour-digitcode that is stored in individualvariables.Theirprogram should provide output containing the numberofcorrectdigitsincorrectlocations,aswellasthenumberofcorrectdigitsin incorrect locations.Thisprogram canbe continuallyimproved as studentslearn about</td></tr><tr><td>3</td><td>3.5</td><td>nestedconditional statementsandcompoundBooleanexpressions. Diagramming</td></tr><tr><td></td><td></td><td>Have students create truth tables by listing all the possible true and false combinationsandcorrespondingBooleanvaluesforagivencompoundBoolean expression.Oncestudentshavecreatedthetruthtable,providestudentswithinput</td></tr><tr><td></td><td></td><td>values.HavestudentsdeterminethevalueofeachindividualBooleanexpressionand usethetruthtabletodeterminetheresultofthecompoundBooleanexpression.</td></tr><tr><td>4</td><td></td><td></td></tr><tr><td></td><td>3.6</td><td>Studentresponsesystem</td></tr></table></body></html>  

# Boolean Expressions and if Statements  

# SUGGESTED SKILL  

Apply the meaning of specific operators.  

# TOPIC 3.1 Boolean Expressions  

# AVAILABLE RESOURCES  

Practice-It!:BJP4 Chapter 4: Conditional Execution—SelfCheck 4.2  

# Required Course Content  

# ENDURING UNDERSTANDING  

# CON-1  

The way variables and operators are sequenced and combined in an expression determines the computed result.  

# LEARNING OBJECTIVE  

# CON-1.E  

Evaluate Boolean expressions that use relational operators in program code.  

# ESSENTIAL KNOWLEDGE  

CON-1.E.1  

Primitive values and reference values can be compared using relational operators (i.e., $==$ and $\!=\rangle$ .  

# CON-1.E.2  

Arithmetic expression values can be compared using relational operators (i.e., $<,>,<=,>=)$ .  

# CON-1.E.3  

An expression involving relational operators evaluates to a Boolean value.  

# TOPIC 3.2 if Statements and Control Flow  

# SUGGESTED SKILLS  

Determine the result or output based on statement execution order in a code segment without method calls (other than output).  

Write program code to satisfy method specifications using expressions, conditional statements, and iterative statements.  

# Required Course Content  

# ENDURING UNDERSTANDING  

# CON-2  

Programmers incorporate iteration and selection into code as a way of providing instructions for the computer to process each of the many possible input values.  

# LEARNING OBJECTIVE ESSENTIAL KNOWLEDGE  

# CON-2.A  

# CON-2.A.1  

Represent branching logical processes by using conditional statements.  

Conditional statements interrupt the sequential execution of statements.  

# CON-2.A.2  

if statements affect the flow of control by executing different statements based on the value of a Boolean expression.  

# CON-2.A.3  

A one-way selection (if statement) is written when there is a set of statements to execute under a certain condition. In this case, the body is executed only when the Boolean condition is true.  

# AVAILABLE RESOURCES  

Runestone Academy: AP CSA—Java Review: 5.1—Conditionals § Practice-It!: BJP4 Chapter 4: Conditional Execution—Self-Check 4.3; Exercises 4.2 and 4.3 The Exam $>$ 2017 AP Computer Science A Exam Free-Response Question #1, Part A (Phrase)  

# Boolean Expressions and if Statements  

# SUGGESTED SKILLS  

Write program code to satisfy method specifications using expressions, conditional statements, and iterative statements.  

# 4.A  

Use test-cases to find errors or validate results.  

![](images/65457ebf11823ced062c7a332661632ff52629779567a8f76ce2d5aa87302414.jpg)  

# AVAILABLE RESOURCES  

Runestone Academy: AP CSA—Java Review: 5.1—Conditionals Practice-It!:BJP4 Chapter 4: Conditional Execution—Self-Check 4.5–4.6, 4.10–4.12  

# TOPIC 3.3 if-else Statements  

# Required Course Content  

# ENDURING UNDERSTANDING  

# CON-2  

Programmers incorporate iteration and selection into code as a way of providing instructions for the computer to process each of the many possible input values.  

# LEARNING OBJECTIVE  

# ESSENTIAL KNOWLEDGE  

# CON-2.A  

# CON-2.A.4  

Represent branching logical processes by using conditional statements.  

A two-way selection is written when there are two sets of statements— one to be executed when the Boolean condition is true, and another set for when the Boolean condition is false. In this case, the body of the “if” is executed when the Boolean condition is true, and the body of the “else” is executed when the Boolean condition is false.  

SUGGESTED SKILLS  

# Required Course Content  

Write program code to satisfy method specifications using expressions, conditional statements, and iterative statements.  

# 4.C  

# TOPIC 3.4 else if Statements  

Determine if two or more code segments yield equivalent results.  

# ENDURING UNDERSTANDING  

![](images/f6ae5fc7eca7116a51e28a4da19cd8ab74712ef93fc8cbc05d48c3b8c3328604.jpg)  

# AVAILABLE RESOURCES  

§ Runestone Academy: AP CSA—Java Review: 5.2—Three or More Options  

# CON-2  

Programmers incorporate iteration and selection into code as a way of providing instructions for the computer to process each of the many possible input values.  

# LEARNING OBJECTIVE ESSENTIAL KNOWLEDGE  

# CON-2.A  

# CON-2.A.5  

Represent branching logical processes by using conditional statements.  

A multi-way selection is written when there are a series of conditions with different statements for each condition. Multi-way selection is performed using if-else-if statements such that exactly one section of code is executed based on the first condition that evaluates to true.  

# Boolean Expressions and if Statements  

# SUGGESTED SKILLS  

Determine the result or output based on statement execution order in a code segment without method calls (other than output).  

Write program code to satisfy method specifications using expressions, conditional statements, and iterative statements.  

# TOPIC 3.5 Compound Boolean Expressions  

# Required Course Content  

# AVAILABLE RESOURCES  

§ Runestone Academy: AP CSA—Java Review: 5.3—Complex Conditionals   
§ Practice-It!: BJP4 Chapter 4: Conditional Execution—Exercise 4.12  

# ENDURING UNDERSTANDING  

# CON-2  

Programmers incorporate iteration and selection into code as a way of providing instructions for the computer to process each of the many possible input values.  

# LEARNING OBJECTIVE ESSENTIAL KNOWLEDGE  

CON-2.B  

CON-2.B.1  

Represent branching logical processes by using nested conditional statements.  

Nested if statements consist of if statements within if statements.  

# ENDURING UNDERSTANDING  

# CON-1  

The way variables and operators are sequenced and combined in an expression determines the computed result.  

# LEARNING OBJECTIVE ESSENTIAL KNOWLEDGE  

# CON-1.F  

# CON-1.F.1  

Evaluate compound Boolean expressions in program code.  

Logical operators !(not), &&(and), and ||(or) are used with Boolean values. This represents the order these operators will be evaluated.  

# CON-1.F.2  

An expression involving logical operators evaluates to a Boolean value.  

# CON-1.F.3  

When the result of a logical expression using && or || can be determined by evaluating only the first Boolean operand, the second is not evaluated. This is known as short-circuited evaluation.  

# TOPIC 3.6 Equivalent Boolean Expressions  

# SUGGESTED SKILL  

# 4.C  

Determine if two or more code segments yield equivalent results.  

![](images/2040424149288b91f4ba8b7b2a88df1df9c93189592bb306527505c86f9a9ee2.jpg)  

# Required Course Content  

# AVAILABLE RESOURCE  

· Runestone Academy: AP CSA—Java Review: 5.5—De Morgan’s Laws  

# ENDURING UNDERSTANDING  

# CON-1  

The way variables and operators are sequenced and combined in an expression determines the computed result.  

# LEARNING OBJECTIVE ESSENTIAL KNOWLEDGE  

# CON-1.G  

# CON-1.G.1  

Compare and contrast equivalent Boolean expressions.  

De Morgan’s Laws can be applied to Boolean expressions.  

# CON-1.G.2  

Truth tables can be used to prove Boolean identities.  

# CON-1.G.3  

Equivalent Boolean expressions will evaluate to the same value in all cases.  

# Boolean Expressions and if Statements  

# SUGGESTED SKILLS  

Determine the result or output based on the statement execution order in a code segment containing method calls.  

Write program code to create objects of a class and call methods.  

# TOPIC 3.7 Comparing Objects  

# Required Course Content  

# ENDURING UNDERSTANDING  

# CON-1  

The way variables and operators are sequenced and combined in an expression determines the computed result.  

# LEARNING OBJECTIVE  

# CON-1.H  

# ESSENTIAL KNOWLEDGE  

# CON-1.H.1  

Compare object references using Boolean expressions in program code.  

Two object references are considered aliases when they both reference the same object.  

# CON-1.H.2  

Object reference values can be compared, using $==$ and $\!=$ , to identify aliases.  

# CON-1.H.3  

A reference value can be compared with null, using $==$ or $\!=$ , to determine if the reference actually references an object.  

# CON-1.H.4  

Often classes have their own equals method, which can be used to determine whether two objects of the class are equivalent.  

# AP COMPUTER SCIENCE A  

# UNIT 4 Iteration  

Remember to go to AP Classroom to assign students the online Personal Progress Check for this unit.  

Whether assigned as homework or completed in class, the Personal Progress Check provides each student with immediate feedback related to this unit’s topics and skills.  

# Personal Progress Check 4  

# Multiple-choice: \~15 questions Free-response: 2 questions  

$\cdot$ Methods and Control Structures $\cdot$ Methods and Control Structures: partial  

![](images/1dafee0753e51ea74b51c61f9b5a4234d9fa63970bd343b2528d386ae38bf1df.jpg)  

<html><body><table><tr><td>17.5-22.5% APEXAMWEIGHTING</td><td>~14-16 CLASSPERIODS</td></tr></table></body></html>  

# Iteration  

# Developing Understanding  

# BIG IDEA 1  

# Control CON  

§ How does iteration improve programs and reduce the amount of program code necessary to complete a task?   
§ What situations would warrant the use of one type of loop over another?  

This unit focuses on iteration using while and for loops. As you saw in Unit 3, Boolean expressions are useful when a program needs to perform different operations under different conditions. Boolean expressions are also one of the main components in iteration. This unit introduces several standard algorithms that use iteration. Knowledge of standard algorithms makes solving similar problems easier, as algorithms can be modified or combined to suit new situations.  

Iteration is used when traversing data structures such as arrays, ArrayLists, and 2D arrays. In addition, it is a necessary component of several standard algorithms, including searching and sorting, which will be covered in later units.  

# Building Computational Thinking Practices  

# 2.B 2.D 3.C 5.C  

Students should be able to determine the result of program code that uses iterative statements to represent nonlinear processes in a program. Students should practice determining the number of times a given loop structure will execute. Spending time analyzing existing program code provides opportunities for students to better understand how iterative structures can be set up and used to solve their own problems, as well as the implications associated with code changes, such as how using a different iterative structure might change the result of a set of program code.  

Students should be able to implement program code that uses iterative statements to represent nonlinear processes. Understanding how to write program code that repeats allows students to write programs to solve a wider variety of problems, including those that use data, which will be covered in Units 6, 7, and 8.  

# Preparing for the AP Exam  

While the concept of iteration is tested in isolation on the multiple-choice exam, it is a foundational concept that students will use along with other topics, such as data structures, on free-response questions. Often, students struggle in situations that warrant variation in the Boolean condition of loops, such as when they want to terminate a loop early. Early termination of a loop requires the use of conditional statements within the body of the loop. If the order of the program statements is incorrect, the early termination may be triggered too early or not at all. Provide students with practice ordering statements by giving them strips of paper, each with a line of program code that can be used to assemble the correct and incorrect solutions. Ask them to reassemble the code and trace it to see if it is correct. Using manipulatives in this way makes it easier for students to rearrange the order of the program code to determine if it is in the correct order.  

![](images/dac42ea6ab111a3729c7be36edb6b4572d85e5a51c2c964617e05e4118d8545d.jpg)  

# Iteration  

<html><body><table><tr><td colspan="2">Topic</td><td>Class Periods</td></tr><tr><td colspan="2">4.1 while Loops</td><td>~14-16 CLASS PERIODS</td></tr><tr><td rowspan="8">4.2 for Loops CON-2 4.3 Developing Algorithms Using Strings</td><td>complete code segments. 2.BDetermine theresult oroutput based on</td><td></td></tr><tr><td>statementexecutionorderin a codesegment without method calls (other than output).</td><td></td></tr><tr><td>3.CWrite program code to satisfy method specifications using expressions,conditional statements,and iterative statements.</td><td></td></tr><tr><td>3.cWrite program code to satisfy method specifications using expressions, conditional statements,and iterative statements.</td><td></td></tr><tr><td>4.cDetermine if two or more code segments yield equivalentresults.</td><td></td></tr><tr><td>5.cExplain howtheresultofprogram code changes, given a change to the initial code.</td><td></td></tr><tr><td>2.CDetermine the result or output based on the statementexecutionorderinacodesegment</td><td></td></tr><tr><td>containing method calls. 3.cWrite program code to satisfy method specifications using expressions,conditional</td><td></td></tr><tr><td colspan="2">4.4 Nested Iteration 4.5 Informal Code Analysis Go to AP Classroom to assign the Personal Progress Check for Unit 4.</td><td>statements,and iterativestatements.</td></tr></table></body></html>  

# SAMPLE INSTRUCTIONAL ACTIVITIES  

The sample activities on this page are optional and are offered to provide possible ways to incorporate instructional approaches into the classroom. They were developed in partnership with teachers from the AP community to share ways that they approach teaching some of the topics in this unit. Please refer to the Instructional Approaches section beginning on p. 159 for more examples of activities and strategies.  

<html><body><table><tr><td>Activity</td><td>Topic</td><td>Sample Activity</td></tr><tr><td>1</td><td>4.2</td><td>Jigsaw As a whole class, look at a code segment containing iteration and the resulting</td></tr><tr><td></td><td></td><td>output.Afterward,divide studentsinto groups,and provide eachgroup witha slightly modified code segment. After groups have determined how the result changes based differentversionofthecodesegmentandsharetheirconclusions.</td></tr><tr><td>2</td><td>4.1-4.4</td><td>Note-taking Provide studentswith a method that,when givenaninteger,returns the month name fromaStringthatincludesallthemonthnamesinorder,eachseparatedbyaspace. Havethem annotatewhateachstatementdoesinthemethod.Then,askstudentsto usetheirannotated method asaguidetowritea similarmethodthat,givenastudent</td></tr><tr><td></td><td></td><td></td></tr><tr><td>3</td><td>4.5</td><td>ofallstudentsintheclass,eachseparatedbyaspace.</td></tr></table></body></html>  

![](images/566523bc6e85011f4fc5f27db4a2e11782b8f2fc4cd5d96bbee774a8f8e8de99.jpg)  

# Unit Planning Notes  

Use the space below to plan your approach to the unit. Consider how you want to pace your course and where you will incorporate writing and analyzing program code.  

After completing this unit, students will have covered all of the necessary content for the Consumer Review Lab. {} The proposed class periods for this unit include time to complete the provided lab activities.  

# SUGGESTED SKILLS  

Determine code that would be used to complete code segments.  

Determine the result or output based on statement execution order in a code segment without method calls (other than output).  

Write program code to satisfy method specifications using expressions, conditional statements, and iterative statements.  

![](images/981dad3f2dd5d95e974079b8d161862c7f1e8a6082bed12ac0dd43851e604f41.jpg)  

# AVAILABLE RESOURCES  

§ Runestone Academy: AP CSA—Java Review: 7.2—While Loops   
·Practice-It!:BJP4 Chapter 5: Program Logic and Indefinite Loops—Exercises 5.1–5.4   
§ The Exam $>$ 2017 AP Computer Science A Exam Free-Response Question #3, Part B (Phrase)  

# Iteration  

# TOPIC 4.1 while Loops  

# Required Course Content  

# ENDURING UNDERSTANDING  

# CON-2  

Programmers incorporate iteration and selection into code as a way of providing instructions for the computer to process each of the many possible input values.  

# LEARNING OBJECTIVE ESSENTIAL KNOWLEDGE  

# CON-2.C  

Represent iterative processes using a while loop.  

# CON-2.C.1  

Iteration statements change the flow of control by repeating a set of statements zero or more times until a condition is met.  

# CON-2.C.2  

In loops, the Boolean expression is evaluated before each iteration of the loop body, including the first. When the expression evaluates to true, the loop body is executed. This continues until the expression evaluates to false, whereupon the iteration ceases.  

# CON-2.C.3  

A loop is an infinite loop when the Boolean expression always evaluates to true.  

# CON-2.C.4  

If the Boolean expression evaluates to false initially, the loop body is not executed at all.  

# CON-2.C.5  

Executing a return statement inside an iteration statement will halt the loop and exit the method or constructor.  

# Iteration  

# LEARNING OBJECTIVE  

# ESSENTIAL KNOWLEDGE  

# CON-2.D  

For algorithms in the context of a particular specification that does not require the use of traversals:  

§ Identify standard algorithms.   
§ Modify standard algorithms.   
§ Develop an algorithm.  

# CON-2.D.1  

There are standard algorithms to:  

· Identify if an integer is or is not evenly divisible by another integer · Identify the individual digits in an integer § Determine the frequency with which a specific criterion is met  

# CON-2.D.2  

There are standard algorithms to:  

§ Determine a minimum or maximum value § Compute a sum, average, or mode  

# SUGGESTED SKILLS 3.C  

Write program code to satisfy method specifications using expressions, conditional statements, and iterative statements.  

Determine if two or more code segments yield equivalent results.  

Explain how the result of program code changes, given a change to the initial code.  

![](images/d47e8016b6152d8c9881ec40bfa7bf42223a7fca2998ef08ee182e5b603c0b18.jpg)  

# AVAILABLE RESOURCES  

Runestone Academy: AP CSA—Java Review: 7.3—For Loops § Practice-It!: BJP4 Chapter 2: Primitive Data and Definite Loops—Exercises 2.2, 2.3  

# Iteration  

# TOPIC 4.2 for Loops  

# Required Course Content  

# ENDURING UNDERSTANDING  

# CON-2  

Programmers incorporate iteration and selection into code as a way of providing instructions for the computer to process each of the many possible input values.  

# LEARNING OBJECTIVE  

# ESSENTIAL KNOWLEDGE  

CON-2.E  

Represent iterative processes using a for loop.  

# CON-2.E.1  

There are three parts in a for loop header: the initialization, the Boolean expression, and the increment. The increment statement can also be a decrement statement.  

# CON-2.E.2  

In a for loop, the initialization statement is only executed once before the first Boolean expression evaluation. The variable being initialized is referred to as a loop control variable.  

# CON-2.E.3  

In each iteration of a for loop, the increment statement is executed after the entire loop body is executed and before the Boolean expression is evaluated again.  

# CON-2.E.4  

A for loop can be rewritten into an equivalent while loop and vice versa.  

# CON-2.E.5  

“Off by one” errors occur when the iteration statement loops one time too many or one time too few.  

# TOPIC 4.3 Developing Algorithms Using Strings  

# Required Course Content  

# SUGGESTED SKILLS  

Determine the result or output based on the statement execution order in a code segment containing method calls.  

Write program code to satisfy method specifications using expressions, conditional statements, and iterative statements.  

# ENDURING UNDERSTANDING  

# CON-2  

Programmers incorporate iteration and selection into code as a way of providing instructions for the computer to process each of the many possible input values.  

# LEARNING OBJECTIVE ESSENTIAL KNOWLEDGE  

# CON-2.F  

# CON-2.F.1  

For algorithms in the context of a particular specification that involves String objects:  

There are standard algorithms that utilize String traversals to:  

§ Find if one or more substrings has a particular property   
§ Determine the number of substrings that meet specific criteria   
§ Create a new string with the characters reversed   
§ Identify standard algorithms.   
§ Modify standard algorithms.   
§ Develop an algorithm.  

# AVAILABLE RESOURCES  

·Practice-lt!: BJP4 Chapter 3: Parameters and Objects—Exercise 3.19   
§ Practice-It!: BJP4 Chapter 5: Program Logic and Indefinite Loops—Exercise 5.24   
§ CodingBat Java: String-2  

# Iteration  

# SUGGESTED SKILLS  

Determine code that would be used to complete code segments.  

# TOPIC 4.4 Nested Iteration  

Write program code to satisfy method specifications using expressions, conditional statements, and iterative statements.  

Explain how the result of program code changes, given a change to the initial code.  

![](images/a8e7994c93d4ef9e1d59fd7867c412f4a508381a5f97d039da5bc8381f3ecf3f.jpg)  

# AVAILABLE LAB  

§ Classroom Resources > AP Computer Science A: Consumer Review Lab  

# AVAILABLE RESOURCES  

· Runestone Academy: AP CSA—Java Review: 7.4—Nested For Loops Practice-It!: BJP4 Chapter 2: Primitive Data and Definite Loops—Exercises 2.4–2.15 · Past AP Free-Response Exam Questions on Methods and Control Structures on AP Question Bank  

# Required Course Content  

# ENDURING UNDERSTANDING  

# CON-2  

Programmers incorporate iteration and selection into code as a way of providing instructions for the computer to process each of the many possible input values.  

# LEARNING OBJECTIVE ESSENTIAL KNOWLEDGE  

CON-2.G  

# CON-2.G.1  

Represent nested iterative processes.  

Nested iteration statements are iteration statements that appear in the body of another iteration statement.  

# CON-2.G.2  

When a loop is nested inside another loop, the inner loop must complete all its iterations before the outer loop can continue.  

# TOPIC 4.5 Informal Code Analysis  

Determine the number of times a code segment will execute.  

# Required Course Content  

# ENDURING UNDERSTANDING  

# CON-2  

Programmers incorporate iteration and selection into code as a way of providing instructions for the computer to process each of the many possible input values.  

# LEARNING OBJECTIVE ESSENTIAL KNOWLEDGE  

# CON-2.H  

# CON-2.H.1  

Compute statement execution counts and informal run-time comparison of iterative statements.  

A statement execution count indicates the number of times a statement is executed by the program.  

# AP COMPUTER SCIENCE A  

UNIT 5  

# Writing Classes  

Remember to go to AP Classroom to assign students the online Personal Progress Check for this unit.  

Whether assigned as homework or completed in class, the Personal Progress Check provides each student with immediate feedback related to this unit’s topics and skills.  

# Personal Progress Check 5  

Multiple-choice: \~25 questions Free-response: 2 questions  

Class Class: partial  

![](images/d1100ff38d7e09240ee1d58b9386a352f14dc7a1c63669e41254c90d3fce1c40.jpg)  

<html><body><table><tr><td>5-7.5 % APEXAMWEIGHTING</td><td>~12-14 CLASSPERIODS</td></tr></table></body></html>  

# Writing Classes  

# Developing Understanding  

# BIG IDEA 1 Modularity MOD  

■ How can using a model of traffic patterns improve travel time?  

# BIG IDEA 2 Variables  VAR  

■ How can programs be written to protect your bank account balance from being inadvertently changed?  

BIG IDEA 3 Impact of Computing IOC § What responsibility do programmers have for the consequences of programs they create, whether intentional or not?  

This unit will pull together information from all previous units to create new, user-defined reference data types in the form of classes. The ability to accurately model real-world entities in a computer program is a large part of what makes computer science so powerful. This unit focuses on identifying appropriate behaviors and attributes of real-world entities and organizing these into classes. Students will build on what they learn in this unit to represent relationships between classes through hierarchies, which appear in Unit 9.  

The creation of computer programs can have extensive impacts on societies, economies, and cultures. The legal and ethical concerns that come with programs and the responsibilities of programmers are also addressed in this unit.  

# Building Computational Thinking Practices  

# 1.A 3.B 5.A 5.B  5.D  

Computer scientists use computers to study and model the world, and this requires designing program code to fit a given scenario. Spending time to plan out the program up front will shorten overall program development time. Practicing elements of the iterative development process early and often will help create more robust programs and avoid logical errors.  

Because revisions to program code are rarely completed by the original author, documenting program code is very important. It allows programmers to more quickly understand how a code segment functions without having to analyze the program code itself. Well-written documentation includes a description of the behavior, as well as the initial conditions that must be met for a code segment to work as intended.  

Sometimes students struggle to explain why a code segment will not compile or work as intended. It helps to have students work with a collaborative partner to practice verbally  

explaining the issues. The ability to explain why a code segment isn’t working correctly assists in the development of solutions.  

# Preparing for the AP Exam  

On the free-response section of the exam, students are required to design program code that demonstrates the functionality available for an object of a new class, based on the prompt’s specification. This process includes identifying the attributes (data) that define an object of a class and the behaviors (methods) that define what an object of a class can do. Students should have many opportunities in this course to design their own classes based on program specifications and on observations of real-world objects.  

Once the new class is designed, students should be able to implement program code to create a new type by creating a class. The behaviors of an object are expressed through writing methods in the class, which include expressions, conditional statements, and iterative statements. By being able to create their own classes, programmers are not limited to the existing classes provided within the Java libraries and can therefore represent their own ideas through classes.  

![](images/ea0c78d88203c4cbfbda59500635aa6095dd9ff30e5b0929b05baa3a31d5b10c.jpg)  

# Writing Classes  

<html><body><table><tr><td colspan="2">Understanding Enduring Suggested Skills</td><td>Class Periods</td></tr><tr><td>Topic 2 3 MOD- D MOI</td><td>5.1 Anatomy of a Class assessed).</td><td>~12-14 CLASS PERIODS 1.ADetermine an appropriate program design tosolveaproblemoraccomplishatask(not</td></tr><tr><td rowspan="7"></td><td>5.2 Constructors</td><td>1.BDetermine code thatwould be used to complete code segments.</td></tr><tr><td>1.C Determinecodethatwouldbeusedtointeract withcompletedprogramcode.</td><td></td></tr><tr><td>3.B I Write program code to define a new type by creating a class. 5.D</td><td></td></tr><tr><td>5.3 Documentation with Comments 5.4AccessorMethods</td><td>IDescribe theinitial conditions that must be met for a programsegment to work as intended or described. 3.B Write program code to define a new type by</td><td></td></tr><tr><td>5.B</td><td>creating a class. I Explain why a code segment will not compile or</td><td></td></tr><tr><td>5.5 Mutator Methods</td><td>work as intended. 3.BWrite program code to define a new type by creating a class.</td><td></td></tr><tr><td></td><td>4.B Identify errors in program code.</td><td></td></tr><tr><td rowspan="2"></td><td>5.6 Writing Methods</td><td>1.B Determinecodethatwouldbeusedto complete code segments.</td><td></td></tr><tr><td>creating a class.</td><td>3.B Write program code to define a new type by</td><td></td></tr><tr><td rowspan="2"></td><td>5.7 Static Variables and Methods</td><td>3.B I Write program code to define a new type by creating a class.</td><td></td></tr><tr><td></td><td>5.A IDescribe the behavior of a given segment of program code.</td><td></td></tr></table></body></html>  

# UNIT AT A GLANCE (cont’d)  

<html><body><table><tr><td>Understanding Enduring</td><td colspan="2">Suggested Skills</td><td>Class Periods</td></tr><tr><td rowspan="4">VAR-1</td><td>Topic 5.8 Scope and Access</td><td>3.B Writeprogramcodetodefine a newtypeby creating a class.</td><td>~12-14 CLASS PERIODS</td></tr><tr><td></td><td>5.BExplain why a code segment will not compile or work as intended.</td><td></td></tr><tr><td>5.9 this Keyword</td><td>2.cDeterminetheresultoroutputbasedonthe statementexecutionorderinacodesegment</td><td></td></tr><tr><td>5.10 Ethical and Social Implications of</td><td>containing method calls. Curricularrequirement,notassessedontheAPExam</td><td></td></tr><tr><td>I0C-1 AP</td><td colspan="2">Computing Systems Go to AP Classroom to assign the Personal Progress Check for Unit 5.</td><td></td></tr></table></body></html>  

![](images/9be1083680fd562daae07bf7f66edfbb28391ca62120265bea98b5259ad7096a.jpg)  

# Writing Classes  

# SAMPLE INSTRUCTIONAL ACTIVITIES  

The sample activities on this page are optional and are offered to provide possible ways to incorporate instructional approaches into the classroom. They were developed in partnership with teachers from the AP community to share ways that they approach teaching some of the topics in this unit. Please refer to the Instructional Approaches section beginning on p. 159 for more examples of activities and strategies.  

<html><body><table><tr><td>Activity</td><td>Topic</td><td>Sample Activity</td></tr><tr><td>1</td><td>5.1</td><td>Kinestheticlearning Havestudentsbreakintogroupsof4-5toplayboardgames.Askthemtoplaythe gameforabout10 minutes.While theyplaythegame,theyshould keeptrackof the variousnounstheyencounterandactionsthathappenaspartofthegame.Thenouns</td></tr><tr><td>2</td><td>5.3</td><td>can berepresented in the computer as classes,and the actions are the behaviors.At theendofgameplay,askstudentstocreateUMLdiagramsfortheidentifiedclasses. Markingthetext</td></tr><tr><td>3</td><td>5.4-5.7</td><td>preconditions(bothimplicitand explicit)thatexistforthemethodtofunction.This Createaplan</td></tr><tr><td></td><td></td><td>theprocessiscorrect and todetermine if anyadditional information is neededbefore beginningtoprogramasolutiononthecomputer.</td></tr><tr><td>4</td><td>5.7 Paraphrase</td><td>Providestudentswithseveralexampleclassesthatutilizestaticvariablesforunique identificationnumbersorforcounting thenumberofobjectsthathavebeencreated,</td></tr></table></body></html>  

# Unit Planning Notes  

Use the space below to plan your approach to the unit. Consider how you want to pace your course and where you will incorporate writing and analyzing program code.  

# TOPIC 5.1 Anatomy of a Class  

# SUGGESTED SKILL  

Determine an appropriate program design to solve a problem or accomplish a task.  

Determine code that would be used to complete code segments.  

# Required Course Content  

![](images/b9f5b7afcf5b7146972f3bfdfa63f62acbc7ec7084e80bc9894738dd59fc38a4.jpg)  

# AVAILABLE RESOURCES  

# ENDURING UNDERSTANDING  

Programmers use code to represent a physical object or nonphysical concept, real or imagined, by defining a class based on the attributes and/or behaviors of the object or concept.  

§ Runestone Academy: AP CSA—Java Review: 2.7—Parts of a Java Class   
§ Practice-It!: BJP4 Chapter 8: Classes— Self-Check 8.1–8.7   
§ Classroom Resources $>$ Object-Oriented Design  

# MOD-2  

# LEARNING OBJECTIVE ESSENTIAL KNOWLEDGE  

# MOD-2.A  

Designate access and visibility constraints to classes, data, constructors, and methods.  

# MOD-2.A.1  

The keywords public and private affect the access of classes, data, constructors, and methods.  

# MOD-2.A.2  

The keyword private restricts access to the declaring class, while the keyword public allows access from classes outside the declaring class.  

# MOD-2.A.3  

Classes are designated public.  

# MOD-2.A.4  

Access to attributes should be kept internal to the class. Therefore, instance variables are designated as private.  

# MOD-2.A.5  

Constructors are designated public.  

# MOD-2.A.6  

Access to behaviors can be internal or external to the class. Therefore, methods can be designated as either public or private.  

# Writing Classes  

# ENDURING UNDERSTANDING  

# MOD-3  

When multiple classes contain common attributes and behaviors, programmers create a new class containing the shared attributes and behaviors forming a hierarchy. Modifications made at the highest level of the hierarchy apply to the subclasses.  

# LEARNING OBJECTIVE ESSENTIAL KNOWLEDGE  

# MOD-3.A  

# MOD-3.A.1  

Designate private visibility of instance variables to encapsulate the attributes of an object.  

Data encapsulation is a technique in which the implementation details of a class are kept hidden from the user.  

# MOD-3.A.2  

When designing a class, programmers make decisions about what data to make accessible and modifiable from an external class. Data can be either accessible or modifiable, or it can be both or neither.  

# MOD-3.A.3  

Instance variables are encapsulated by using the private access modifier.  

# MOD-3.A.4  

The provided accessor and mutator methods in a class allow client code to use and modify data.  

# TOPIC 5.2 Constructors  

# Required Course Content  

# ENDURING UNDERSTANDING  

# MOD-2  

Programmers use code to represent a physical object or nonphysical concept, real or imagined, by defining a class based on the attributes and/or behaviors of the object or concept.  

![](images/e4d3e6cb451ff9807d33fdb1d789bf5b59464312f685d1fb2ef2a410e615c462.jpg)  

# LEARNING OBJECTIVE ESSENTIAL KNOWLEDGE  

# MOD-2.B  

Define instance variables for the attributes to be initialized through the constructors of a class.  

An object’s state refers to its attributes and their values at a given time and is defined by instance variables belonging to the object. This creates a “has-a” relationship between the object and its instance variables.  

# MOD-2.B.2  

Constructors are used to set the initial state of an object, which should include initial values for all instance variables.  

# MOD-2.B.3  

Constructor parameters are local variables to the constructor and provide data to initialize instance variables.  

# MOD-2.B.4  

When a mutable object is a constructor parameter, the instance variable should be initialized with a copy of the referenced object. In this way, the instance variable is not an alias of the original object, and methods are prevented from modifying the state of the original object.  

# MOD-2.B.5  

When no constructor is written, Java provides a no-argument constructor, and the instance variables are set to default values.  

# MOD-2.B.1  

# SUGGESTED SKILLS  

Determine code that would be used to interact with completed program code.  

Write program code to define a new type by creating a class.  

![](images/08b4bcd7a848630fb4d1e6b6b58cc0b044d59e8855b49775821b1fda2b14987c.jpg)  

# AVAILABLE RESOURCES  

§ Runestone Academy: AP CSA—Java Review: 2.7—Parts of a Java Class § Practice-It!: BJP4 Chapter 8: Classes— Exercises 8.14–8.22  

# SUGGESTED SKILL  

Describe the initial conditions that must be met for a program segment to work as intended or described.  

# TOPIC 5.3 Documentation with Comments  

# AVAILABLE RESOURCE  

External Resource $>$ Zeroturnaround: Reasons, Tips and Tricks for Better Java Documentation  

# Required Course Content  

# ENDURING UNDERSTANDING  

# MOD-2  

Programmers use code to represent a physical object or nonphysical concept, real or imagined, by defining a class based on the attributes and/or behaviors of the object or concept.  

# LEARNING OBJECTIVE ESSENTIAL KNOWLEDGE  

# MOD-2.C  

Describe the functionality and use of program code through comments.  

# MOD-2.C.1  

Comments are ignored by the compiler and are not executed when the program is run.  

# MOD-2.C.2  

Three types of comments in Java include $/\star\star/$ , which generates a block of comments, $//$ , which generates a comment on one line, and $/\star\star\star/\$ , which are Javadoc comments and are used to create API documentation.  

# MOD-2.C.3  

A precondition is a condition that must be true just prior to the execution of a section of program code in order for the method to behave as expected. There is no expectation that the method will check to ensure preconditions are satisfied.  

# MOD-2.C.4  

A postcondition is a condition that must always be true after the execution of a section of program code. Postconditions describe the outcome of the execution in terms of what is being returned or the state of an object.  

# MOD-2.C.5  

Programmers write method code to satisfy the postconditions when preconditions are met.  

# TOPIC 5.4 Accessor Methods  

# SUGGESTED SKILLS  

Write program code to define a new type by creating a class.  

Explain why a code segment will not compile or work as intended.  

# Required Course Content  

![](images/5d055b72714e07b40be9387644119978630ec03fcdfc557986548dfa8c00d9a6.jpg)  

# AVAILABLE LABS  

# ENDURING UNDERSTANDING  

# MOD-2  

Classroom Resources $>$ ·AP Computer Science A: Data Lab AP Computer Science A: Celebrity Lab  

Programmers use code to represent a physical object or nonphysical concept, real or imagined, by defining a class based on the attributes and/or behaviors of the object or concept.  

# AVAILABLE RESOURCE  

·Practice-It!: BJP4 Chapter 8: Classes— Exercises 8.14–8.22  

# LEARNING OBJECTIVE ESSENTIAL KNOWLEDGE  

# MOD-2.D  

Define behaviors of an object through non-void methods without parameters written in a class.  

# MOD-2.D.1  

An accessor method allows other objects to obtain the value of instance variables or static variables.  

# MOD-2.D.2  

A non-void method returns a single value. Its header includes the return type in place of the keyword void.  

# MOD-2.D.3  

In non-void methods, a return expression compatible with the return type is evaluated, and a copy of that value is returned. This is referred to as “return by value.”  

# MOD-2.D.4  

When the return expression is a reference to an object, a copy of that reference is returned, not a copy of the object.  

# MOD-2.D.5  

The return keyword is used to return the flow of control to the point immediately following where the method or constructor was called.  

# Writing Classes  

# LEARNING OBJECTIVE ESSENTIAL KNOWLEDGE  

MOD-2.D  

# MOD-2.D.6  

Define behaviors of an object through non-void methods without parameters written in a class.  

The toString method is an overridden method that is included in classes to provide a description of a specific object. It generally includes what values are stored in the instance data of the object.  

# MOD-2.D.7  

If System.out.print or System.out. println is passed an object, that object’s toString method is called, and the returned string is printed.  

# TOPIC 5.5 Mutator Methods  

# SUGGESTED SKILLS  

Write program code to define a new type by creating a class.  

Identify errors in program code.  

![](images/3dc44dbeb75ec07afee415175d77e1877871c334881a6996ca58039a06b18b6c.jpg)  

# Required Course Content  

# AVAILABLE RESOURCE  

§ Practice-It!: BJP4 Chapter 8: Classes— Exercises 8.14–8.22  

# ENDURING UNDERSTANDING  

# MOD-2  

Programmers use code to represent a physical object or nonphysical concept, real or imagined, by defining a class based on the attributes and/or behaviors of the object or concept.  

# LEARNING OBJECTIVE ESSENTIAL KNOWLEDGE  

# MOD-2.E  

Define behaviors of an object through void methods with or without parameters written in a class.  

# MOD-2.E.1  

A void method does not return a value. Its header contains the keyword void before the method name.  

# MOD-2.E.2  

A mutator (modifier) method is often a void method that changes the values of instance variables or static variables.  

# SUGGESTED SKILLS 1.B  

Determine code that would be used to complete code segments.  

Write program code to define a new type by creating a class.  

![](images/5813349460561e94ebb27ac172b5bd6191b8fb5ce48356fd9340217d41e6e26b.jpg)  

# AVAILABLE RESOURCES  

§ Practice-It!: BJP4 Chapter 3: Parameters and Objects— Exercises 3.1–3.22 Practice-lt!: BJP4 Chapter 8: Class Exercises 8.14-8.22  

# TOPIC 5.6 Writing Methods  

# Required Course Content  

# ENDURING UNDERSTANDING  

# MOD-2  

Programmers use code to represent a physical object or nonphysical concept, real or imagined, by defining a class based on the attributes and/or behaviors of the object or concept.  

# LEARNING OBJECTIVE ESSENTIAL KNOWLEDGE  

# MOD-2.F  

# MOD-2.F.1  

Define behaviors of an object through non-void methods with parameters written in a class.  

Methods can only access the private data and methods of a parameter that is a reference to an object when the parameter is the same type as the method’s enclosing class.  

# MOD-2.F.2  

Non-void methods with parameters receive values through parameters, use those values, and return a computed value of the specified type.  

# MOD-2.F.3  

It is good programming practice to not modify mutable objects that are passed as parameters unless required in the specification.  

# MOD-2.F.4  

When an actual parameter is a primitive value, the formal parameter is initialized with a copy of that value. Changes to the formal parameter have no effect on the corresponding actual parameter.  

# Writing Classes  

# LEARNING OBJECTIVE ESSENTIAL KNOWLEDGE  

MOD-2.F  

# MOD-2.F.5  

Define behaviors of an object through non-void methods with parameters written in a class.  

When an actual parameter is a reference to an object, the formal parameter is initialized with a copy of that reference, not a copy of the object. If the reference is to a mutable object, the method or constructor can use this reference to alter the state of the object.  

# MOD-2.F.6  

Passing a reference parameter results in the formal parameter and the actual parameter being aliases. They both refer to the same object.  

# SUGGESTED SKILLS  

Write program code to define a new type by creating a class.  

Describe the behavior of a given segment of program code.  

# TOPIC 5.7 Static Variables and Methods  

# Required Course Content  

# ENDURING UNDERSTANDING  

# MOD-2  

Programmers use code to represent a physical object or nonphysical concept, real or imagined, by defining a class based on the attributes and/or behaviors of the object or concept.  

# LEARNING OBJECTIVE ESSENTIAL KNOWLEDGE  

# MOD-2.G  

Define behaviors of a class through static methods.  

# MOD-2.G.1  

Static methods are associated with the class, not objects of the class.  

# MOD-2.G.2  

Static methods include the keyword static in the header before the method name.  

# MOD-2.G.3  

Static methods cannot access or change the values of instance variables.  

# MOD-2.G.4  

Static methods can access or change the values of static variables.  

# MOD-2.G.5  

Static methods do not have a this reference and are unable to use the class’s instance variables or call non-static methods.  

# MOD-2.H  

Define the static variables that belong to the class.  

# MOD-2.H.1  

Static variables belong to the class, with all objects of a class sharing a single static variable.  

# Writing Classes  

# LEARNING OBJECTIVE ESSENTIAL KNOWLEDGE  

MOD-2.H  

# MOD-2.H.2  

Define the static variables that belong to the class.  

Static variables can be designated as either public or private and are designated with the static keyword before the variable type.  

# MOD-2.H.3  

Static variables are used with the class name and the dot operator, since they are associated with a class, not objects of a class.  

# SUGGESTED SKILLS  

# TOPIC 5.8  

Explain why a code segment will not compile or work as intended.  

# Scope and Access  

Write program code to define a new type by creating a class.  

# Required Course Content  

# ENDURING UNDERSTANDING  

# VAR-1  

To find specific solutions to generalizable problems, programmers include variables in their code so that the same algorithm runs using different input values.  

# LEARNING OBJECTIVE ESSENTIAL KNOWLEDGE  

# VAR-1.G  

# VAR-1.G.1  

Explain where variables can be used in the program code.  

Local variables can be declared in the body of constructors and methods. These variables may only be used within the constructor or method and cannot be declared to be public or private.  

# VAR-1.G.2  

When there is a local variable with the same name as an instance variable, the variable name will refer to the local variable instead of the instance variable.  

# VAR-1.G.3  

Formal parameters and variables declared in a method or constructor can only be used within that method or constructor.  

# VAR-1.G.4  

Through method decomposition, a programmer breaks down a large problem into smaller subproblems by creating methods to solve each individual subproblem.  

# TOPIC 5.9 this Keyword  

# SUGGESTED SKILL 2.C  

Determine the result or output based on the statement execution order in a code segment containing method calls.  

# Required Course Content  

# AVAILABLE RESOURCE  

§ Past AP Free-Response Exam Questions on Class on AP Question Bank  

# ENDURING UNDERSTANDING  

# VAR-1  

To find specific solutions to generalizable problems, programmers include variables in their code so that the same algorithm runs using different input values.  

# LEARNING OBJECTIVE ESSENTIAL KNOWLEDGE  

# VAR-1.H  

# VAR-1.H.1  

Evaluate object reference expressions that use the keyword this.  

Within a non-static method or a constructor, the keyword this is a reference to the current object—the object whose method or constructor is being called.  

# VAR-1.H.2  

The keyword this can be used to pass the current object as an actual parameter in a method call.  

# TOPIC 5.10 Ethical and Social Implications of Computing Systems  

# AVAILABLE RESOURCE  

· Classroom Resources $>$ Ethical Use of the Computer  

Required Course Content  

# ENDURING UNDERSTANDING  

# IOC-1  

While programs are typically designed to achieve a specific purpose, they may have unintended consequences.  

# LEARNING OBJECTIVE ESSENTIAL KNOWLEDGE  

IOC-1.A  

Explain the ethical and social implications of computing systems.  

IOC-1.A.1  

System reliability is limited. Programmers should make an effort to maximize system reliability.  

# IOC-1.A.2  

Legal issues and intellectual property concerns arise when creating programs.  

# IOC-1.A.3  

The creation of programs has impacts on society, economies, and culture. These impacts can be beneficial and/or harmful.  

# AP COMPUTER SCIENCE A  

UNIT 6 Array  

Remember to go to AP Classroom to assign students the online Personal Progress Check for this unit.  

Whether assigned as homework or completed in class, the Personal Progress Check provides each student with immediate feedback related to this unit’s topics and skills.  

# Personal Progress Check 6  

# Multiple-choice: \~15 questions Free-response: 2 questions  

Array and ArrayList (Array only) Array and ArrayList (Array only): partial  

![](images/7e0b82c2fae26c16d79a39c850e1be264a82b18cb082afbab37520aee0e9a6e2.jpg)  

<html><body><table><tr><td>10-15% APEXAMWEIGHTING</td><td>~6-8 CLASSPERIODS</td></tr></table></body></html>  

# Array  

# Developing Understanding  

# BIG IDEA 1  

# Variables VAR  

■ How can programs leverage volcano data to make predictions about the date of the next eruption?  

# BIG IDEA 2 Control  CON  

§ How can knowing standard algorithms be useful when solving new problems?  

This unit focuses on data structures, which are used to represent collections of related data using a single variable rather than multiple variables. Using a data structure along with iterative statements with appropriate bounds will allow for similar treatment to be applied more easily to all values in the collection. Just as there are useful standard algorithms when dealing with primitive data, there are standard algorithms to use with data structures. In this unit, we apply standard algorithms to arrays; however, these same algorithms are used with ArrayLists and 2D arrays as well. Additional standard algorithms, such as standard searching and sorting algorithms, will be covered in the next unit.  

# Building Computational Thinking Practices  

# 3.D 4.B  

Students should be able to implement program code to create, traverse, and manipulate elements in a 1D array. Traversing elements of a 1D array can be accomplished in multiple ways. Programmers need to make decisions about which loop structure is most effective given the problem they are trying to solve. Some loop structures, such as the enhanced for loop, only allow programmers to examine the data stored in a 1D array structure, while other loop structures allow the data to be manipulated.  

Students should be able to identify and correct errors related to traversing and manipulating 1D array structures. A common run-time error that programmers experience is an out-of-bounds error, which occurs when the program tries to access an element that is beyond the range of elements in a collection. Students should double-check the values of the index being used on at least the initial and final loop iterations to ensure that they aren’t out of bounds.  

# Preparing for the AP Exam  

A specific iterative structure is commonly used to traverse an array: starting at the beginning and moving toward the last element in the array. When students are asked to determine the result of program code that contains arrays, they often use this same iterative structure. Knowing this iterative structure can be helpful when students use tracing to determine what an algorithm is doing. Students can follow this traversal for the first few iterations and apply that pattern to the remaining elements in the array.  

When preparing for the free-response questions, students should be come familiar with how existing algorithms work, rather than just memorizing the program code. Have students write out an algorithm on paper and test it using manipulatives. This allows students to experience the algorithm on a deeper level than if they simply program it. A strong understanding of how existing algorithms work allows programmers to make modifications to those algorithms to accomplish similar tasks.  

![](images/069e6eee3db2b30c03645ed2278d4f7190152bfcec9b9bf7e92d31377400b5c8.jpg)  

# Array  

<html><body><table><tr><td colspan="2">Understanding Topic</td><td>Suggested Skills</td><td>Class Periods</td></tr><tr><td rowspan="7">VAR-2</td><td>6.1 Array Creation and Access</td><td>1.CDetermine code that would be used to interact with completed program code.</td><td>~6-8 CLASS PERIODS</td></tr><tr><td>6.2 Traversing Arrays</td><td>3.D Write program code to create, traverse, and manipulateelementsin1DarrayorArrayList objects. 2.BDetermine the result or output based on</td><td></td></tr><tr><td></td><td>statementexecutionorderinacodesegment without method calls (other than output). 3.DWrite program code to create, traverse, and manipulateelementsin1D arrayorArrayList</td><td></td></tr><tr><td></td><td>objects. 4.B Identify errors in program code.</td><td></td></tr><tr><td>6.3 Enhanced for Loop for Arrays</td><td>3.D Write program code to create, traverse, and</td><td></td></tr><tr><td></td><td>manipulate elements in 1D array or ArrayList objects. 4.C Determine if two or more code segments yield</td><td></td></tr><tr><td>6.4 Developing Algorithms Using Arrays</td><td>equivalentresults. 1.BDetermine code thatwould beused to complete code segments.</td><td></td></tr><tr><td rowspan="2">CON-2</td><td></td><td>3.DWrite program code to create, traverse, and manipulate elements in 1D array or ArrayList</td><td></td></tr><tr><td>objects. 5.D or described.</td><td>Describe the initial conditions thatmust be metfora programsegmentto workas intended</td><td></td></tr><tr><td>AP</td><td>Go to AP Classroom to assign the Personal Progress Check for Unit 6.</td><td>Review the results in class to identify and address any student misunderstandings.</td><td></td></tr></table></body></html>  

# SAMPLE INSTRUCTIONAL ACTIVITIES  

The sample activities on this page are optional and are offered to provide possible ways to incorporate instructional approaches into the classroom. They were developed in partnership with teachers from the AP community to share ways that they approach teaching some of the topics in this unit. Please refer to the Instructional Approaches section beginning on p. 159 for more examples of activities and strategies.  

<html><body><table><tr><td>Activity</td><td>Topic</td><td>Sample Activity</td></tr><tr><td>1</td><td>6.1</td><td>Diagramming Provide students with several prompts to create and access elements in an array. Aftertheyhavedeterminedthecodeforeachprompt,havestudentsdrawamemory</td></tr><tr><td>2</td><td>6.2</td><td>diagramthatshowsreferencesandthearraystheypointto.Havestudentsupdatethe diagramwitheachstatementtodemonstratehowchangingthecontentsthroughone array reference effects all the array references for this array. Erroranalysis</td></tr><tr><td></td><td></td><td>Providestudentswithseveral error-riddencodesegmentscontaining arraytraversals type up their solutions in an IDE toverify their work.</td></tr><tr><td>3</td><td>6.3</td><td>Think-pair-share Askstudentsto consider two program code segments that are meantto yield the</td></tr><tr><td></td><td></td><td>themtakeafewminutestothinkindependentlyaboutwhetherthetwosegments accomplishthesameresult and,if not,whatchangescouldbemade inorderforthat where it would make sense to use one type of loop over the other before sharing with</td></tr></table></body></html>  

# SUGGESTED SKILLS  

Determine code that would be used to interact with completed program code.  

Write program code to create, traverse, and manipulate elements in 1D array or ArrayList objects.  

# AVAILABLE RESOURCES  

§ Runestone Academy: AP CSA—Java Review: 8.1—Arrays in Java ·Practice-It!: BJP4 Chapter 7: Array— Self-Check 7.1–7.9 § CodingBat Java: Array-1  

# Array  

# TOPIC 6.1 Array Creation and Access  

# Required Course Content  

# ENDURING UNDERSTANDING  

# VAR-2  

To manage large amounts of data or complex relationships in data, programmers write code that groups the data together into a single data structure without creating individual variables for each value.  

# LEARNING OBJECTIVE ESSENTIAL KNOWLEDGE  

# VAR-2.A  

# VAR-2.A.1  

Represent collections of related primitive or object reference data using onedimensional (1D) array objects.  

The use of array objects allows multiple related items to be represented using a single variable.  

# VAR-2.A.2  

The size of an array is established at the time of creation and cannot be changed.  

# VAR-2.A.3  

Arrays can store either primitive data or object reference data.  

# VAR-2.A.4  

When an array is created using the keyword new, all of its elements are initialized with a specific value based on the type of elements:  

· Elements of type int are initialized to 0   
· Elements of type double are initialized to 0 . 0   
· Elements of type boolean are initialized to false   
· Elements of a reference type are initialized to the reference value null. No objects are automatically created  

# VAR-2.A.5  

Initializer lists can be used to create and initialize arrays.  

# Array  

# LEARNING OBJECTIVE ESSENTIAL KNOWLEDGE  

# VAR-2.A  

# VAR-2.A.6  

Represent collections of related primitive or object reference data using onedimensional (1D) array objects.  

Square brackets ([ ]) are used to access and modify an element in a 1D array using an index.  

# VAR-2.A.7  

The valid index values for an array are 0 through one less than the number of elements in the array, inclusive. Using an index value outside of this range will result in an ArrayIndexOutOfBoundsException being thrown.  

# Array  

# SUGGESTED SKILLS  

Determine the result or output based on statement execution order in a code segment without method calls (other than output).  

Write program code to create, traverse, and manipulate elements in 1D array or ArrayList objects.  

# TOPIC 6.2 Traversing Arrays  

Identify errors inprogram code.  

# Required Course Content  

![](images/ef566499f07712fbd9f57440ed139c660606769b2a576c762a703f3b2fd24fd4.jpg)  

# ENDURING UNDERSTANDING  

# AVAILABLE RESOURCES VAR-2  

· Runestone Academy: AP CSA—Java Review: 8.3—Using a For Loop to Loop through an Array CodingBat Java: Array-2 Practice-It!: BJP4 Chapter 7: Arrays— Exercise 7.1–7.18  

To manage large amounts of data or complex relationships in data, programmers write code that groups the data together into a single data structure without creating individual variables for each value.  

# LEARNING OBJECTIVE ESSENTIAL KNOWLEDGE  

# VAR-2.B  

Traverse the elements in a 1D array.  

# VAR-2.B.1  

Iteration statements can be used to access all the elements in an array. This is called traversing the array.  

# VAR-2.B.2  

Traversing an array with an indexed for loop or while loop requires elements to be accessed using their indices.  

# VAR-2.B.3  

Since the indices for an array start at 0 and end at the number of elements - 1, "off by one" errors are easy to make when traversing an array, resulting in an ArrayIndexOutOfBoundsException being thrown.  

![](images/4a75bb778f51516b67dbff43368f49abb343d25172afd72d2ae663771c9cd915.jpg)  

# TOPIC 6.3 Enhanced for Loop for Arrays  

# Required Course Content  

Write program code to create, traverse, and manipulate elements in 1D array or ArrayList objects.  

# 4.C  

Determine if two or more code segments yield equivalent results.  

# SUGGESTED SKILLS  

# ENDURING UNDERSTANDING  

# VAR-2  

To manage large amounts of data or complex relationships in data, programmers write code that groups the data together into a single data structure without creating individual variables for each value.  

# AVAILABLE RESOURCES  

Runestone Academy: AP CSA—Java Review: 8.2—Looping with the For-Each Loop Practice-It!: BJP4 Chapter 7: Arrays— Exercises 7.1–7.18  

# LEARNING OBJECTIVE ESSENTIAL KNOWLEDGE  

# VAR-2.C  

Traverse the elements in a 1D array object using an enhanced for loop.  

# VAR-2.C.1  

An enhanced for loop header includes a variable, referred to as the enhanced for loop variable.  

# VAR-2.C.2  

For each iteration of the enhanced for loop, the enhanced for loop variable is assigned a copy of an element without using its index.  

# VAR-2.C.3  

Assigning a new value to the enhanced for loop variable does not change the value stored in the array.  

# VAR-2.C.4  

Program code written using an enhanced for loop to traverse and access elements in an array can be rewritten using an indexed for loop or a while loop.  

# SUGGESTED SKILLS  

Determine code that would be used to complete code segments.  

Write program code to create, traverse, and manipulate elements in 1D array or ArrayList objects.  

Describe the initial conditions that must be met for a program segment to work as intended or described.  

# AVAILABLE RESOURCES  

Runestone Academy: AP CSA—Java Review: 8.13—Free-Response Questions · CodingBat Java: Array 3 Practice-It!:BJP4 Chapter 7: Array— Exercises 7.1–7.18  

# Array  

# TOPIC 6.4 Developing Algorithms Using Arrays  

# Required Course Content  

# ENDURING UNDERSTANDING  

# CON-2  

Programmers incorporate iteration and selection into code as a way of providing instructions for the computer to process each of the many possible input values.  

# LEARNING OBJECTIVE ESSENTIAL KNOWLEDGE  

# CON-2.I  

For algorithms in the context of a particular specification that requires the use of array traversals:  

§ Identify standard algorithms.   
§ Modify standard algorithms.   
§ Develop an algorithm.  

# CON-2.I.1  

There are standard algorithms that utilize array traversals to:  

§ Determine a minimum or maximum value   
§ Compute a sum, average, or mode   
§ Determine if at least one element has a particular property   
§ Determine if all elements have a particular property   
§ Access all consecutive pairs of elements   
§ Determine the presence or absence of duplicate elements   
§ Determine the number of elements meeting specific criteria  

# CON-2.I.2  

There are standard array algorithms that utilize traversals to:  

§ Shift or rotate elements left or right § Reverse the order of the elements  

# AP COMPUTER SCIENCE A  

UNIT 7  

ArrayList  

Remember to go to AP Classroom to assign students the online Personal Progress Check for this unit.  

Whether assigned as homework or completed in class, the Personal Progress Check provides each student with immediate feedback related to this unit’s topics and skills.  

# Personal Progress Check 7  

Multiple-choice: \~15 questions Free-response: 1 question  

$\cdot$ Array and ArrayList (ArrayList focus)  

![](images/db4f1dd8308a1ee9781cab5085776dbaca21d996e08cf9ab805766db3e9a4219.jpg)  

<html><body><table><tr><td>2.5-7.5 % APEXAMWEIGHTING</td><td>~10-12 CLASSPERIODS</td></tr></table></body></html>  

# ArrayList  

# Developing Understanding  

# BIG IDEA 1 Variables  VAR  

· Why is an ArrayList more appropriate for storing your music playlist, while an array might be more appropriate for storing your class schedule?  

# BIG IDEA 2 Control  CON  

§ How can we use statement execution counts to choose appropriate algorithms?  

BIG IDEA 3 Impact of Computing  IOC § What personal data is currently being collected, and how?  

As students learned in Unit 6, data structures are helpful when storing multiple related data values. Arrays have a static size, which causes limitations related to the number of elements stored, and it can be challenging to reorder elements stored in arrays. The ArrayList object has a dynamic size, and the class contains methods for insertion and deletion of elements, making reordering and shifting items easier. Deciding which data structure to select becomes increasingly important as the size of the data set grows, such as when using a large real-world data set.  

In this unit, students will also learn about privacy concerns related to storing large amounts of personal data and about what can happen if such information is compromised.  

# Building Computational Thinking Practices  

# 2.C 2.D 3.D 5.C  

Students need to consider the impact using ArrayList rather than an array has on the structure of their program code. This includes considering the use of ArrayList methods and the flexibility of a structure with a dynamic size. For instance, the use of an ArrayList will require students to analyze program code that uses method calls.  

Providing students with practice writing programs for data sets of undetermined sized—or at least larger than they would be able to analyze easily by hand—presents a more relevant and realistic experience with data. Additionally, this requires students to focus more on the algorithm and ensuring that it will work in all situations rather than on an individual result.  

With larger data sets, programmers become concerned with the amount of time it will take for their program code to run. Students should have practice determining the number of times a code segment executes; this can help them gain an idea of how long it will take to run a program on a data set of a given size.  

# Preparing for the AP Exam  

When writing solutions to free-response questions that involve the use of an ArrayList, students are often asked to insert or delete elements from the ArrayList. In these cases, adjustments will need to be made to the loop counter to account for skipping an element or attempting to access elements that no longer exist.  

Students may also be asked to traverse multiple data structures simultaneously. These data structures may be a mixture of array and ArrayList objects. As such, it is very easy for students to become confused about how elements are accessed and manipulated within each structure. Additionally, the size of the data structures may not be the same. In these situations, it is best to have different index variables and bounds checks for each structure to avoid accessing elements that are out-of-bounds.  

![](images/b85d0831efde6dfdf7154efb9faf4bc03a9ede15b6e6601f30ac280a4eebe569.jpg)  

# ArrayList  

<html><body><table><tr><td>Understanding Enduring</td><td colspan="2"></td><td>Class Periods</td></tr><tr><td rowspan="7">VAR-2</td><td rowspan="2">Topic 7.1 Introduction to ArrayList</td><td>Suggested Skills 1.BDetermine code thatwouldbe used to</td><td>~10-12 CLASS PERIODS</td></tr><tr><td>complete code segments. 3.D Write program code to create,traverse, and manipulate elements in1D array or</td><td></td></tr><tr><td rowspan="2">7.2 ArrayList Methods</td><td>2.cDetermine the result or output based on the statementexecutionorderina codesegment containing method calls.</td><td></td></tr><tr><td>3.D Write program code to create,traverse, and manipulate elements in 1D array or ArrayList objects.</td><td></td></tr><tr><td>7.3 Traversing ArrayLists</td><td>2.cDetermine theresult or output based on the statementexecution orderinacode segment containing method calls.</td><td></td></tr><tr><td rowspan="2">7.4 Developing Algorithms</td><td>3.D Writeprogramcodetocreate,traverse, and manipulate elements in 1D array or ArrayList objects.</td><td rowspan="2"></td></tr><tr><td>3.D Writeprogramcodetocreate,traverse, and manipulate elements in 1D array or ArrayList objects.</td></tr><tr><td rowspan="2">CON-2 7.5 Searching</td><td rowspan="2">4.A 3.D</td><td>Use test-cases tofind errors orvalidateresults. Write program code to create,traverse,</td><td></td></tr><tr><td>and manipulate elements in 1D array or ArrayList objects. 5.CExplain how the result of program code</td><td></td></tr><tr><td></td><td>7.6 Sorting</td><td>changes, given a change to the initial code. 2.DDetermine the number of times a code</td><td></td></tr><tr><td>C-1</td><td>7.7 Ethical Issues Around</td><td>segment will execute. Curricular requirement, not assessed on the AP Exam</td><td></td></tr><tr><td>0</td><td>Data Collection</td><td></td><td></td></tr></table></body></html>  

Go to AP Classroom to assign the Personal Progress Check for Unit 7.   
Review the results in class to identify and address any student misunderstandings.  

# SAMPLE INSTRUCTIONAL ACTIVITIES  

The sample activities on this page are optional and are offered to provide possible ways to incorporate instructional approaches into the classroom. They were developed in partnership with teachers from the AP community to share ways that they approach teaching some of the topics in this unit. Please refer to the Instructional Approaches section beginning on p. 159 for more examples of activities and strategies.  

<html><body><table><tr><td>Activity</td><td>Topic</td><td>Sample Activity</td></tr><tr><td>1</td><td>7.2</td><td>Predictandcompare Havestudentslookatthecodetheywrotetosolvethefree-responsequestion inUnit6 (or other code from Unit 6) on paper, and have them rewrite it using an ArrayList. Have them highlight the parts that need to be changed and determine how to change them.Then,have students type up the changes in an IDE and confirm that the</td></tr><tr><td>2</td><td>7.1-7.5</td><td>programstillworksasexpected. Identifyasubtask Have students read through an ArrayList-based free-response question in groups, and havethemidentifyallsubtasks.Thesesubtaskscouldbeconditional statements, iteration, or even other methods.Once the subtasks have beenidentified, divide the subtasks among the group members, and have students implement their given</td></tr><tr><td></td><td></td><td>subtask.When all students arefinished,have them combine the subtasksintoa single solution.</td></tr><tr><td>3</td><td>7.5</td><td>Discussion group Discuss the algorithm necessaryto search for the smallest valuein anArrayList.</td></tr></table></body></html>  

# Unit Planning Notes  

Use the space below to plan your approach to the unit. Consider how you want to pace your course and where you will incorporate writing and analyzing program code that uses real-world data sets.  

# SUGGESTED SKILLS  

Determine code that would be used to complete code segments.  

Write program code to create, traverse, and manipulate elements in 1D array or ArrayList objects.  

# AVAILABLE RESOURCES  

■ Java Quick Reference (see Appendix)   
Runestone Academy: AP CSA—Java Review: 9.7—The ArrayList Class   
§ Practice-It!: BJP4 Chapter 10: ArrayLists—SelfCheck 10.2  

# TOPIC 7.1 Introduction to ArrayList  

# Required Course Content  

# ENDURING UNDERSTANDING  

# VAR-2  

To manage large amounts of data or complex relationships in data, programmers write code that groups the data together into a single data structure without creating individual variables for each value.  

# LEARNING OBJECTIVE  

VAR-2.D  

# ESSENTIAL KNOWLEDGE  

VAR-2.D.1  

Represent collections of related object reference data using ArrayList objects.  

An ArrayList object is mutable and contains object references.  

VAR-2.D.2  

The ArrayList constructor ArrayList() constructs an empty list.  

# VAR-2.D.3  

Java allows the generic type ArrayList $<\mathtt{E}>$ , where the generic type E specifies the type of the elements.  

# VAR-2.D.4  

When ArrayList ${<}\mathtt{E}{>}$ is specified, the types of the reference parameters and return type when using the methods are type E.  

# VAR-2.D.5  

ArrayList $<\mathtt{E}>$ is preferred over ArrayList because it allows the compiler to find errors that would otherwise be found at run-time.  

# TOPIC 7.2 ArrayList Methods  

# SUGGESTED SKILLS  

# 2.C  

Determine the result or output based on the statement execution order in a code segment containing method calls.  

Write program code to create, traverse, and manipulate elements in 1D array or ArrayList objects.  

# Required Course Content  

# ENDURING UNDERSTANDING  

# VAR-2  

To manage large amounts of data or complex relationships in data, programmers write code that groups the data together into a single data structure without creating individual variables for each value.  

# LEARNING OBJECTIVE ESSENTIAL KNOWLEDGE  

# VAR-2.D  

# VAR-2.D.6  

Represent collections of related object reference data using ArrayList objects.  

The ArrayList class is part of the java. util package. An import statement can be used to make this class available for use in the program.  

# VAR-2.D.7  

The following ArrayList methods— including what they do and when they are used—are part of the Java Quick Reference:  

int size()-Returns the number of elements in the list   
boolean add(E obj)-Appends obj to end of list; returns true   
void add(int index, E obj)- Inserts obj at position index ( $0\quad<=$ index $<=$ size), moving elements at position index and higher to the right (adds 1 to their indices) and adds 1 to size   
E get(int index)-Returnsthe element at position index in the list   
E set(int index，E obj)— Replaces the element at position index with obj; returns the element formerly at position index  

# AVAILABLE RESOURCES  

■ Java Quick Reference (see Appendix)   
Practice-It!: BJP4 Chapter 10: ArrayLists—Exercises 10.2–10.17 The Exam $>$ 2017 AP Computer Science A Exam Free-Response Question #1, Part A (Digits)  

# ArrayList  

# LEARNING OBJECTIVE  

VAR-2.D  

Represent collections of related object reference data using ArrayList objects.  

# ESSENTIAL KNOWLEDGE  

· E remove(int index)-Removes element from position index, moving elements at position index $^+\beth$ and higher to the left (subtracts 1 from their indices) and subtracts 1 from size; returns the element formerly at position index  

# TOPIC 7.3 Traversing ArrayLists  

# SUGGESTED SKILLS  

Determine the result or output based on the statement execution order in a code segment containing method calls.  

Write program code to create, traverse, and manipulate elements in 1D array or ArrayList objects.  

# Required Course Content  

# ENDURING UNDERSTANDING  

# VAR-2  

To manage large amounts of data or complex relationships in data, programmers write code that groups the data together into a single data structure without creating individual variables for each value.  

# AVAILABLE RESOURCES  

· Runestone Academy: AP CSA—Java Review: 9.14—Looping through a List   
§ Practice-It!: BJP4 Chapter 10: ArrayLists—Exercises 10.2–10.17   
The Exam $>$ 2018 AP Computer Science A Exam Free-Response Question #2 (WordPair)  

# LEARNING OBJECTIVE ESSENTIAL KNOWLEDGE  

# VAR-2.E  

For ArrayList objects:  

a. Traverse using a for or while loop b. Traverse using an enhanced for loop  

# VAR-2.E.1  

Iteration statements can be used to access all the elements in an ArrayList. This is called traversing the ArrayList.  

# VAR-2.E.2  

Deleting elements during a traversal of an ArrayList requires using special techniques to avoid skipping elements.  

# VAR-2.E.3  

Since the indices for an ArrayList start at 0 and end at the number of elements - 1, accessing an index value outside of this range will result in an ArrayIndexOutOfBoundsException being thrown.  

# VAR-2.E.4  

Changing the size of an ArrayList   
while traversing it using an   
enhanced for loop can result in a   
ConcurrentModificationException being thrown. Therefore, when using   
an enhanced for loop to traverse an   
ArrayList, you should not add or   
remove elements.  

# SUGGESTED SKILLS  

Write program code to create, traverse, and manipulate elements in 1D array or ArrayList objects.  

# 4.A  

Use test-cases to find errors or validate results.  

![](images/8f40b96a13dee43d9f1d6c515338709c1bcdbf4ea6a2a96f22f21116b68f9b1e.jpg)  

AVAILABLE LAB § Classroom Resources > AP Computer Science A: Data Lab  

# AVAILABLE RESOURCES  

·Runestone Academy: AP CSA—Java Review: 9.13—Removing an Object at an Index   
§ Practice-It!: BJP4 Chapter 10: ArrayLists—Exercises 10.2–10.17   
§ The Exam $>$ ·2017 AP Computer Science A Exam Free-Response Question 1, Part B (Digits) ■ Past AP FreeResponse Exam Questions on Array/ ArrayList on AP Question Bank  

# TOPIC 7.4 Developing Algorithms Using ArrayLists  

# Required Course Content  

# ENDURING UNDERSTANDING  

# CON-2  

Programmers incorporate iteration and selection into code as a way of providing instructions for the computer to process each of the many possible input values.  

# LEARNING OBJECTIVE ESSENTIAL KNOWLEDGE  

For algorithms in the context of a particular specification that requires the use of ArrayList traversals:  

CON-2.J  

§ Identify standard algorithms.   
§ Modify standard algorithms.   
§ Develop an algorithm.  

# CON-2.J.1  

There are standard ArrayList algorithms that utilize traversals to:  

· Insert elements   
· Delete elements   
· Apply the same standard algorithms that are used with 1D arrays  

# CON-2.J.2  

Some algorithms require multiple String, array, or ArrayList objects to be traversed simultaneously.  

# TOPIC 7.5 Searching  

# SUGGESTED SKILLS  

Write program code to create, traverse, and manipulate elements in 1D array or ArrayList objects.  

Explain how the result of program code changes, given a change to the initial code.  

# Required Course Content  

# AVAILABLE RESOURCES  

# CON-2  

# ENDURING UNDERSTANDING  

Programmers incorporate iteration and selection into code as a way of providing instructions for the computer to process each of the many possible input values.  

·Practice-It!: BJP4 Chapter 10: ArrayLists—Exercises 10.2–10.17   
§ Runestone Academy: AP CSA—Java Review: 13—Searching and Sorting   
Practice-It!:BJP4 Chapter 13: Searching and Sorting  

# LEARNING OBJECTIVE ESSENTIAL KNOWLEDGE  

# CON-2.K  

CON-2.K.1  

Apply sequential/linear search algorithms to search for specific information in array or ArrayList objects.  

There are standard algorithms for searching.  

# CON-2.K.2  

Sequential/linear search algorithms check each element in order until the desired value is found or all elements in the array or ArrayList have been checked.  

# SUGGESTED SKILL  

Determine the number of times a code segment will execute.  

# TOPIC 7.6 Sorting  

![](images/42225fb216e8f155a544ff275a4d8e1912b819c69100edc3d777d1bcfb434ae0.jpg)  

# AVAILABLE LAB  

·Classroom Resources $>$ AP Computer Science A: Data Lab  

# AVAILABLE RESOURCES  

· Runestone Academy: AP CSA—Java Review: 13—Searching and Sorting   
Practice-It!: BJP4 Chapter 13: Searching and Sorting—SelfCheck 13.29 and 13.30   
§ Visualgo.net: Sorting   
§ Sorting.at  

# Required Course Content  

# ENDURING UNDERSTANDING  

# CON-2  

Programmers incorporate iteration and selection into code as a way of providing instructions for the computer to process each of the many possible input values.  

# LEARNING OBJECTIVE ESSENTIAL KNOWLEDGE  

CON-2.L  

CON-2.L.1  

Apply selection sort and insertion sort algorithms to sort the elements of array or ArrayList objects.  

Selection sort and insertion sort are iterative sorting algorithms that can be used to sort elements in an array or ArrayList.  

# CON-2.M  

Compute statement execution counts and informal run-time comparison of sorting algorithms.  

# CON-2.M.1  

Informal run-time comparisons of program code segments can be made using statement execution counts.  

# TOPIC 7.7 Ethical Issues Around Data Collection  

# Required Course Content  

# AVAILABLE RESOURCES  

# ENDURING UNDERSTANDING  

# IOC-1  

While programs are typically designed to achieve a specific purpose, they may have unintended consequences.  

Classroom Resources $>$   
§ Ethical Use of the Computer   
· Ethical Issues: Internet Content Providers and Internet Service Providers  

# LEARNING OBJECTIVE ESSENTIAL KNOWLEDGE  

# IOC-1.B  

IOC-1.B.1  

Explain the risks to privacy from collecting and storing personal data on computer systems.  

When using the computer, personal privacy is at risk. Programmers should attempt to safeguard personal privacy.  

# IOC-1.B.2  

Computer use and the creation of programs have an impact on personal security. These impacts can be beneficial and/or harmful.  

# AP COMPUTER SCIENCE A  

# UNIT 8 2D Array  

Remember to go to AP Classroom to assign students the online Personal Progress Check for this unit.  

Whether assigned as homework or completed in class, the Personal Progress Check provides each student with immediate feedback related to this unit’s topics and skills.  

# Personal Progress Check 8  

Multiple-choice: \~10 questions Free-response: 1 question  

2D Array  

![](images/6e3d7e9e405a19901f52fa8c67adc636d6422f63f58a09b88d9d33a1f129c4f3.jpg)  

<html><body><table><tr><td>7.5-10 % APEXAMWEIGHTING</td><td>~10-12 CLASSPERIODS</td></tr></table></body></html>  

# 2D Array  

# Developing Understanding  

# BIG IDEA 1  

# Variables VAR  

§ Why might you want to use a 2D array to store the spaces on a game board or the pixels in a picture, rather than a 1D array or ArrayList?  

# BIG IDEA 2 Control CON  

· Why does the order in which elements are accessed in 2D array traversal matter in some situations?  

In Unit 6, students learned how 1D arrays store large amounts of related data. These same concepts will be implemented with two-dimensional (2D) arrays in this unit. A 2D array is most suitable to represent a table. Each table element is accessed using the variable name and row and column indices. Unlike 1D arrays, 2D arrays require nested iterative statements to traverse and access all elements. The easiest way to accomplished this is in row-major order, but it is important to cover additional traversal patterns, such as back and forth or column-major.  

# Building Computational Thinking Practices  

# 1.B 2.B 2.D 3.E  

Students should be able to determine the result of program code that traverses and manipulates the elements in a 2D array. Traversals of 2D arrays typically require a set of nested loops. Often the extra dimension of a 2D array is difficult for students to envision. Providing students with practice analyzing and tracing traversals of a 2D array, as well as providing them partial program code to complete, helps students take this more abstract concept and make it concrete and replicable.  

# Preparing for the AP Exam  

Because 2D arrays are traversed using nested loops, the number of times a code segment executes is multiplied. In a nested loop, the inner loop must complete all iterations before the outer loop can continue. It helps to provide students with sample code that will print the values in a 2D array. Teachers can an IDE that shows access to 2D arrays visually and keeps track of the execution count.  

The free-response portion of the exam always includes one question that requires students to write program code involving 2D arrays. Because 2D arrays are arrays where each element is an array, it is not uncommon for the question to require students to write solutions involving array or ArrayList objects as well.  

While there is a specific nested structure to traverse elements in a 2D array in rowmajor order, this structure can be modified to traverse 2D arrays in other ways, such as column-major, by switching the nested iterative statements. Additional modifications can be made to traverse rows or columns in different ways, such as back and forth or up and down. However, when making these adjustments, students often neglect to adjust the bounds of the iterative statements appropriately. Students should practice traversing 2D arrays in these nonstandard ways, being sure to test the boundary conditions of the iterative statements, to be prepared for this type of freeresponse question.  

![](images/16c33a5f378f3e4556ede2ed7633a1ffa46bb0cb33da89e39bddfb22ac102d16.jpg)  

# 2D Array  

<html><body><table><tr><td rowspan="2">Understanding Enduring</td><td colspan="2"></td><td>Class Periods</td></tr><tr><td>Topic 8.1 2D Arrays 1.B</td><td>Suggested Skills Determinecodethatwouldbeusedto complete code segments.</td><td>~10-12 CLASS PERIODS</td></tr><tr><td>VAR-2</td><td>8.2 Traversing 2D Arrays</td><td>1.cDeterminecodethatwouldbeusedtointeract with completed program code. 3.EWriteprogramcodetocreate,traverse,and manipulate elements in 2D array objects.</td><td></td></tr><tr><td>VAR-2, CON-2</td><td></td><td>2.BDetermine theresultor outputbased on statementexecutionorderinacodesegment without method calls (other than output). 2.DDetermine the numberof timesacode segmentwillexecute. 3.EWriteprogramcodetocreate,traverse,and manipulateelementsin2Darrayobjects. 4.AUse test-cases to find errors or validate results.</td><td></td></tr><tr><td>AP</td><td colspan="2">Go to AP Classroom to assign the Personal Progress Check for Unit 8. Review the results in class to identify and address any student misunderstandings.</td><td></td></tr></table></body></html>  

# SAMPLE INSTRUCTIONAL ACTIVITIES  

The sample activities on this page are optional and are offered to provide possible ways to incorporate instructional approaches into the classroom. They were developed in partnership with teachers from the AP community to share ways that they approach teaching some of the topics in this unit. Please refer to the Instructional Approaches section beginning on p. 159 for more examples of activities and strategies.  

<html><body><table><tr><td>Activity</td><td>Topic</td><td>Sample Activity</td></tr><tr><td>1</td><td>8.1</td><td>Using manipulatives Use different-sized egg cartons or ice cube trays with random compartments filled</td></tr><tr><td></td><td></td><td>withsmalltoysorcandy.Createlaminatedcardswiththecodefortheconstruction of, and access to, a 2D array, leaving blanks for the name and size dimensions.Have studentsfill inthemissingcode thatwouldbeused torepresentthephysical 2D array objectsandaccesstherandomlystoredelements.</td></tr><tr><td>2</td><td>8.2</td><td>Activatingpriorknowledge When first introducing 2D arrays and row-major traversal, ask students which part of</td></tr><tr><td></td><td></td><td>thenestedforloopstructureloopsovera1Darray.Basedonwhattheyknowabout</td></tr><tr><td></td><td></td><td>thetraversalof1Darraystructures,askthemtocalculatethenumberof timesthe</td></tr><tr><td>3</td><td></td><td>inner loop executes.</td></tr></table></body></html>  

![](images/c452bac43a56ba6790a463889b06362ad4dfb4366232dba8fe49c176c5608586.jpg)  

# Unit Planning Notes  

Use the space below to plan your approach to the unit. Consider how you want to pace your course and where you will incorporate writing and analyzing program code that represents 2D data sets.  

After completing this unit, students will have covered all of the necessary content for the Steganography Lab. {} The proposed class periods for this unit include time to complete the provided lab activities.  

![](images/2f5eb7267ada9642b72f4e4d01d2f9685c0369e86f5ddba387378889cb556f4b.jpg)  

# SUGGESTED SKILLS  

Determine code that would be used to complete code segments.  

Determine code that would be used to interact with completed program code.  

Write program code to create, traverse, and manipulate elements in 2D array objects.  

![](images/61c48a9bc4b516f431ce61a9bc3c97c81816a9ebb56f706b589170a682c87935.jpg)  

# AVAILABLE LABS  

Classroom Resources $>$   
·AP Computer Science A: Picture Lab   
·AP Computer Science A: Steganography Lab  

# AVAILABLE RESOURCES  

§ Runestone Academy: AP CSA—Java Review: 10—Two-dimensional Arrays   
§ Practice-It!: BJP4 Chapter 7: Arrays— Self-Check 7.31–7.35   
§ Classroom Resources > GridWorld Resources: A Curriculum Module for AP Computer Science  

# 2D Array  

# TOPIC 8.1 2D Arrays  

# Required Course Content  

# ENDURING UNDERSTANDING  

# VAR-2  

To manage large amounts of data or complex relationships in data, programmers write code that groups the data together into a single data structure without creating individual variables for each value.  

# LEARNING OBJECTIVE ESSENTIAL KNOWLEDGE  

# VAR-2.F  

# VAR-2.F.1  

Represent collections of related primitive or object reference data using two-dimensional (2D) array objects.  

2D arrays are stored as arrays of arrays. Therefore, the way 2D arrays are created and indexed is similar to 1D array objects.  

X  EXCLUSION STATEMENT—(EK VAR-2.F.1): 2D array objects that are not rectangular are outside the scope of the course and AP Exam.  

# VAR-2.F.2  

For the purposes of the exam, when accessing the element at arr[first][second], the first index is used for rows, the second index is used for columns.  

# VAR-2.F.3  

The initializer list used to create and initialize a 2D array consists of initializer lists that represent 1D arrays.  

# VAR-2.F.4  

The square brackets [row][col] are used to access and modify an element in a 2D array.  

# VAR-2.F.5  

“Row-major order” refers to an ordering of 2D array elements where traversal occurs across each row, while “column-major order” traversal occurs down each column.  

# TOPIC 8.2  

# SUGGESTED SKILLS  

# Traversing 2D Arrays  

Determine the result or output based on statement execution order in a code segment without method calls (other than output).  

Determine the number of times a code segment will execute.  

# Required Course Content  

Write program code to create, traverse, and manipulate elements in 2D array objects.  

# ENDURING UNDERSTANDING  

# VAR-2  

# 4.A  

Use test-cases to find errors or validate results.  

To manage large amounts of data or complex relationships in data, programmers write code that groups the data together into a single data structure without creating individual variables for each value.  

# LEARNING OBJECTIVE ESSENTIAL KNOWLEDGE  

# VAR-2.G  

For 2D array objects:  

· Traverse using nested for loops. § Traverse using nested enhanced for loops.  

# VAR-2.G.1  

Nested iteration statements are used to traverse and access all elements in a 2D array. Since 2D arrays are stored as arrays of arrays, the way 2D arrays are traversed using for loops and enhanced for loops is similar to 1D array objects.  

# VAR-2.G.2  

Nested iteration statements can be written to traverse the 2D array in “row-major order” or “column-major order.”  

# VAR-2.G.3  

The outer loop of a nested enhanced for loop used to traverse a 2D array traverses the rows. Therefore, the enhanced for loop variable must be the type of each row, which is a 1D array. The inner loop traverses a single row. Therefore, the inner enhanced for loop variable must be the same type as the elements stored in the 1D array.  

# AVAILABLE LABS  

Classroom Resources >   
§ AP Computer Science A: Picture Lab   
·AP Computer Science A: Steganography Lab  

# AVAILABLE RESOURCES  

§ Runestone Academy: AP CSA—Java Review: 10.7—Looping through a 2D Array   
§ Practice-It!: BJP4 Chapter 7: Arrays— Exercises 7.19–7.19   
§ The Exam > § 2017 AP Computer Science A Exam Free-Response Question #4 (Position) § 2018 AP Computer Science A Exam Free-Response Question #4 (ArrayTester) § Past AP Exam Questions on 2D Arrays on AP Question Bank  

# 2D Array  

# ENDURING UNDERSTANDING  

# CON-2  

Programmers incorporate iteration and selection into code as a way of providing instructions for the computer to process each of the many possible input values.  

# LEARNING OBJECTIVE ESSENTIAL KNOWLEDGE  

CON-2.N  

For algorithms in the context of a particular specification that requires the use of 2D array traversals:  

§ Identify standard algorithms.   
§ Modify standard algorithms.   
§ Develop an algorithm.  

# CON-2.N.1  

When applying sequential/linear search algorithms to 2D arrays, each row must be accessed then sequential/linear search applied to each row of a 2D array.  

# CON-2.N.2  

All standard 1D array algorithms can be applied to 2D array objects.  

# AP COMPUTER SCIENCE A  

# UNIT 9  

# Inheritance  

Remember to go to AP Classroom to assign students the online Personal Progress Check for this unit.  

Whether assigned as homework or completed in class, the Personal Progress Check provides each student with immediate feedback related to this unit’s topics and skills.  

# Personal Progress Check 9  

Multiple-choice: \~15 questions Free-response: 2 questions  

Class Class: partial  

![](images/14f4379dbfa62edca254b0084ebf1185fba0f93234cee566e93f71485b052332.jpg)  

<html><body><table><tr><td>5-10° % APEXAMWEIGHTING</td><td>~13-15 CLASSPERIODS</td></tr></table></body></html>  

# Inheritance  

# Developing Understanding  

# BIG IDEA 1Modularity  MOD  

· How might the use of inheritance help in writing a program that simulates crops being grown in a virtual world? · How does inheritance make programs more versatile?  

Creating objects, calling methods on the objects created, and being able to define a new data type by creating a class are essential understandings before moving into this unit. One of the strongest advantages of Java is the ability to categorize classes into hierarchies through inheritance. Certain existing classes can be extended to include new behaviors and attributes without altering existing code. These newly created classes are called subclasses. In this unit, students will learn how to recognize common attributes and behaviors that can be used in a superclass and will then create a hierarchy by writing subclasses to extend a superclass. Recognizing and utilizing existing hierarchies will help students create more readable and maintainable programs.  

# Building Computational Thinking Practices  

# 1.A 1.C  3.A 3.B  5.A 5.B  5.D  

Students can design hierarchies by listing the attributes and behaviors for each object and pulling common elements into a superclass, leaving unique attributes and behaviors in the subclass. By creating a hierarchy system, students only need to write common program code one time, reducing potential errors and implementation time. This also allows for changes to be made more easily, because they can be made at the superclass level in the hierarchy and automatically apply to subclasses.  

During the development of a program, programmers often use comments to describe the behavior of a given segment of program code and to describe the initial conditions that are used. Students who develop the skill of explaining why program code does not work, such as methods being overloaded improperly or superclass objects attempting to call subclass methods, are much better equipped to foresee and avoid these hierarchy issues.  

# Preparing for the AP Exam  

One question on the free-response section of the exam will require students to write a class. This class could be part of an inheritance relationship. When overriding superclass methods in a subclass, method signatures must be the same. This includes the number, type, and order of any parameters of the overridden method. It is important for students to recognize when a method should be overridden, as well as when they can and should use methods from the superclass. Students who duplicate code unnecessarily will not earn full points on this question.  

Students will be asked to analyze program code that uses inheritance. In many cases, students struggle with determining whether a method is available to be called by an object of a class. When a method is called on a subclass object, the method that is executed is determined during run-time. If the subclass does not contain the called method, the superclass method will automatically be executed.  

![](images/d2b656f7245f107653c423ba352ed5c7d5a1bde31c760d6ab1fdda519e3efcd0.jpg)  

# Inheritance  

<html><body><table><tr><td colspan="2">Understanding</td><td>Class Periods</td></tr><tr><td>9.1 Creating Superclasses and Subclasses</td><td>1.A Determine an appropriate program design to solve aproblem or accomplisha task</td><td>~13-15 CLASS PERIODS</td></tr><tr><td></td><td>3.B Write program code to define a new type by creating a class.</td><td></td></tr><tr><td>9.2 Writing Constructors for Subclasses</td><td>3.B Write program code to define a new type by creating a class.</td><td></td></tr><tr><td></td><td>5.ADescribe the behavior of a given segment of program code.</td><td></td></tr><tr><td>9.3 Overriding Methods</td><td>3.BWrite program code to define a new type by creating a class.</td><td></td></tr><tr><td></td><td>5.D Describe the initial conditions that must be met for a program segment to work as intended or described.</td><td></td></tr><tr><td>9.4 super Keyword</td><td>1.cDetermine code that would be used to interact with completed program code.</td><td></td></tr><tr><td></td><td>3.BWrite program code to define a new type by creating a class.</td><td></td></tr><tr><td>9.5 Creating References Using Inheritance Hierarchies</td><td>3.A Writeprogram code to create objects of a class and call methods.</td><td></td></tr><tr><td></td><td>5.B Explain why a code segment will not compile or work as intended.</td><td></td></tr><tr><td>9.6 Polymorphism</td><td>3.A Write program code to create objects of a class and call methods.</td><td></td></tr><tr><td></td><td>5.BExplain why a code segment will not compile or work as intended.</td><td></td></tr><tr><td>9.7 0bject Superclass</td><td>1.cDeterminecode thatwould beused to interact with completed program code.</td><td></td></tr><tr><td></td><td></td><td></td></tr><tr><td></td><td>3.BWrite program code to define a new type by creating a class.</td><td></td></tr></table></body></html>  

# SAMPLE INSTRUCTIONAL ACTIVITIES  

The sample activities on this page are optional and are offered to provide possible ways to incorporate instructional approaches into the classroom. They were developed in partnership with teachers from the AP community to share ways that they approach teaching some of the topics in this unit. Please refer to the Instructional Approaches section beginning on p. 159 for more examples of activities and strategies.  

<html><body><table><tr><td>Activity</td><td>Topic</td><td>SampleActivity</td></tr><tr><td>1</td><td>9.1</td><td>Activatingpriorknowledge Havestudentsreviewwhattheyknowaboutclasses,methods,and thescopeof variablesbyhavingthemwriteaclassbasedonspecificationsthatcaneasilybe</td></tr><tr><td>2</td><td>9.2-9.4</td><td>writelaterintheunit. Create a plan Given a class design problem thatrequires the use of multiple classes in an inheritance hierarchy, studentsidentify the common attributes and behaviors among these classes and writetheseinto asuperclass.Any additional information that does notbelong in</td></tr><tr><td>3</td><td>9.4</td><td>thesuperclasswillbecategorizedtodeterminetheadditionalclassesthatmightbe necessaryandwhatmethodswillneedtobeaddedoroverriddeninthesubclasses. Think aloud keyword.Have studentsdescribethe codesegmentout loud tothemselves.Give studentsseveral individual statements that attempttointeractwith the givencode</td></tr><tr><td>4</td><td>9.5-9.6</td><td>segment,and havethemtalkthrougheachone,describing whichstatementswould work and which ones would not, aswell as thereasons why those statementswouldn't work. Studentresponsesystem Providestudentswithseveral statementswhereobjectsarecreated andthereference type and object typeare differentbutrelated.Thenprovide students withcallsto methods onthese created objects.Use a studentresponse system tohavestudents</td></tr></table></body></html>  

# Unit Planning Notes  

Use the space below to plan your approach to the unit. Consider how you want to pace your course and where you will incorporate writing and analyzing program code.  

After completing this unit, students will have covered all of the necessary content for the Celebrity Lab. {} The proposed class periods for this unit include time to complete the provided lab activities.  

# SUGGESTED SKILLS  

Determine an appropriate program design to solve a problem or accomplish a task.  

Write program code to define a new type by creating a class.  

![](images/777ec81ecab91d25b7d81f9d210d3bc6664c774b5be09286dff7466c09e49220.jpg)  

# AVAILABLE RESOURCES  

·Runestone Academy: AP CSA—Java Review: 11.3—Inheritance   
· Classroom Resources $>$ ·Object-Oriented Design · An Introduction to Polymorphism in Java  

# Inheritance  

# TOPIC 9.1 Creating Superclasses and Subclasses  

# Required Course Content  

# ENDURING UNDERSTANDING  

# MOD-3  

When multiple classes contain common attributes and behaviors, programmers create a new class containing the shared attributes and behaviors forming a hierarchy. Modifications made at the highest level of the hierarchy apply to the subclasses.  

# LEARNING OBJECTIVE ESSENTIAL KNOWLEDGE  

MOD-3.B  

# MOD-3.B.1  

Create an inheritance relationship from a subclass to the superclass.  

A class hierarchy can be developed by putting common attributes and behaviors of related classes into a single class called a superclass.  

# MOD-3.B.2  

Classes that extend a superclass, called subclasses, can draw upon the existing attributes and behaviors of the superclass without repeating these in the code.  

# MOD-3.B.3  

Extending a subclass from a superclass creates an “is-a” relationship from the subclass to the superclass.  

# MOD-3.B.4  

The keyword extends is used to establish an inheritance relationship between a subclass and a superclass. A class can extend only one superclass.  

# TOPIC 9.2 Writing Constructors for Subclasses  

# SUGGESTED SKILLS  

Write program code to define a new type by creating a class.  

Describe the behavior of a given segment of program code.  

![](images/e6ed783cc306f747320253546ba31d47e022b815af24306529e7d0e6bbf98c07.jpg)  

# Required Course Content  

# AVAILABLE RESOURCES  

# ENDURING UNDERSTANDING  

# MOD-3  

§ Practice-It!: BJP4 Chapter 9: Inheritance and Interfaces—SelfCheck 9.3 Classroom Resources $>$ § An Introduction to Polymorphism in Java § Gradebook Project  

When multiple classes contain common attributes and behaviors, programmers create a new class containing the shared attributes and behaviors forming a hierarchy. Modifications made at the highest level of the hierarchy apply to the subclasses.  

# LEARNING OBJECTIVE ESSENTIAL KNOWLEDGE  

# MOD-3.B  

Create an inheritance relationship from a subclass to the superclass.  

MOD-3.B.5  

Constructors are not inherited.  

# MOD-3.B.6  

The superclass constructor can be called from the first line of a subclass constructor by using the keyword super and passing appropriate parameters.  

# MOD-3.B.7  

The actual parameters passed in the call to the superclass constructor provide values that the constructor can use to initialize the object’s instance variables.  

# MOD-3.B.8  

When a subclass’s constructor does not explicitly call a superclass’s constructor using super, Java inserts a call to the superclass’s no-argument constructor.  

# MOD-3.B.9  

Regardless of whether the superclass constructor is called implicitly or explicitly, the process of calling superclass constructors continues until the Object constructor is called. At this point, all of the constructors within the hierarchy execute beginning with the Object constructor.  

# SUGGESTED SKILLS  

Write program code to define a new type by creating a class.  

# 5.D  

Describe the initial conditions that must be met for a program segment to work as intended or described.  

# AVAILABLE RESOURCES  

·Runestone Academy: AP CSA—Java Review: 11.8—Overriding vs Overloading   
Practice-It!:BJP4 Chapter 9: Inheritance and Interfaces— Exercises 9.4, 9.9   
§ Classroom Resources > An Introduction to Polymorphism in Java Gradebook Project  

# TOPIC 9.3 Overriding Methods  

# Required Course Content  

# ENDURING UNDERSTANDING  

# MOD-3  

When multiple classes contain common attributes and behaviors, programmers create a new class containing the shared attributes and behaviors forming a hierarchy. Modifications made at the highest level of the hierarchy apply to the subclasses.  

# LEARNING OBJECTIVE ESSENTIAL KNOWLEDGE  

MOD-3.B  

# MOD-3.B.10  

Create an inheritance relationship from a subclass to the superclass.  

Method overriding occurs when a public method in a subclass has the same method signature as a public method in the superclass.  

# MOD-3.B.11  

Any method that is called must be defined within its own class or its superclass.  

# MOD-3.B.12  

A subclass is usually designed to have modified (overridden) or additional methods or instance variables.  

# MOD-3.B.13  

A subclass will inherit all public methods from the superclass; these methods remain public in the subclass.  

# TOPIC 9.4 super Keyword  

# SUGGESTED SKILLS  

Determine code that would be used to interact with completed program code.  

Write program code to define a new type by creating a class.  

![](images/444862c29ee7c0cfecbae7fb991b969cfff3e3f36220187fe0aa2548e2db3eda.jpg)  

# Required Course Content  

# AVAILABLE RESOURCES  

# ENDURING UNDERSTANDING  

# MOD-3  

When multiple classes contain common attributes and behaviors, programmers create a new class containing the shared attributes and behaviors forming a hierarchy. Modifications made at the highest level of the hierarchy apply to the subclasses.  

# LEARNING OBJECTIVE ESSENTIAL KNOWLEDGE  

# MOD-3.B  

# MOD-3.B.14  

The keyword super can be used to call a superclass’s constructors and methods.  

Create an inheritance relationship from a subclass to the superclass.  

# MOD-3.B.15  

The superclass method can be called in a subclass by using the keyword super with the method name and passing appropriate parameters.  

· Runestone Academy: AP CSA—Java Review: 11.9—Using Super to Call an Overridden Method   
Classroom Resources > · Gradebook Project § Inheritance and Polymorphism with Sudoku  

# SUGGESTED SKILLS  

Write program code to create objects of a class and call methods.  

Explain why a code segment will not compile or work as intended.  

![](images/da85d9a3173d0d80f65cdf8beb8d2e1288fde7fb29be325eebe83b278a5bac95.jpg)  

# AVAILABLE RESOURCES  

§ Practice-It!: BJP4 Chapter 9: Inheritance and Interfaces—SelfCheck 9.8, 9.10 ·Classroom Resources $>$ Gradebook Project  

# TOPIC 9.5 Creating References Using Inheritance Hierarchies  

Required Course Content  

# ENDURING UNDERSTANDING  

# MOD-3  

When multiple classes contain common attributes and behaviors, programmers create a new class containing the shared attributes and behaviors forming a hierarchy. Modifications made at the highest level of the hierarchy apply to the subclasses.  

# LEARNING OBJECTIVE ESSENTIAL KNOWLEDGE  

# MOD-3.C  

MOD-3.C.1  

Define reference variables of a superclass to be assigned to an object of a subclass in the same hierarchy.  

When a class S “is-a” class T, T is referred to as a superclass, and S is referred to as a subclass.  

# MOD-3.C.2  

If S is a subclass of T, then assigning an object of type S to a reference of type T facilitates polymorphism.  

# MOD-3.C.3  

If S is a subclass of T, then a reference of type T can be used to refer to an object of type T or S.  

# MOD-3.C.4  

Declaring references of type T, when S is a subclass of T, is useful in the following declarations:  

§ Formal method parameters § arrays — T[] var ArrayList<T> var  

![](images/3e0b866926e5458b0486881e7643863942d8dc642ce6555bb519424007ffdab5.jpg)  

# TOPIC 9.6 Polymorphism  

# SUGGESTED SKILLS  

Write program code to create objects of a class and call methods.  

Explain why a code segment will not compile or work as intended.  

![](images/169635a066b0c7a959380e733ecd28c58938447ae807ee46c083ce92fdb7aa94.jpg)  

# Required Course Content  

# AVAILABLE LAB  

Classroom Resources > AP Computer Science A: Celebrity Lab  

# ENDURING UNDERSTANDING  

# MOD-3  

When multiple classes contain common attributes and behaviors, programmers create a new class containing the shared attributes and behaviors forming a hierarchy. Modifications made at the highest level of the hierarchy apply to the subclasses.  

# AVAILABLE RESOURCES  

Runestone Academy: AP CSA—Java Review: 11.15—Polymorphism Practice-It!:BJP4 Chapter 9: Inheritance and Interfaces—SelfCheck 9.9  

# LEARNING OBJECTIVE ESSENTIAL KNOWLEDGE  

# MOD-3.D  

Call methods in an inheritance relationship.  

MOD-3.D.1  

Utilize the Object class through inheritance.  

# MOD-3.D.2  

At compile time, methods in or inherited by the declared type determine the correctness of a non-static method call.  

# MOD-3.D.3  

At run-time, the method in the actual object type is executed for a non-static method call.  

![](images/cdba052e057e7ab11a57d1d26707d29883e54176a8fe7bec6cf5e5c9553f865f.jpg)  

# SUGGESTED SKILLS  

Determine code that would be used to interact with completed program code.  

Write program code to define a new type by creating a class.  

![](images/1f25487f1b269333f8c70e822e9f2cfdb1aae2537c0c8e52e4139b42a73f7bdd.jpg)  

AVAILABLE LAB § Classroom Resources $>$ AP Computer Science A: Celebrity Lab  

AVAILABLE RESOURCE · Java Quick Reference (see Appendix)  

# Inheritance  

# TOPIC 9.7 Object Superclass  

# Required Course Content  

# ENDURING UNDERSTANDING  

# MOD-3  

When multiple classes contain common attributes and behaviors, programmers create a new class containing the shared attributes and behaviors forming a hierarchy. Modifications made at the highest level of the hierarchy apply to the subclasses.  

# LEARNING OBJECTIVE ESSENTIAL KNOWLEDGE  

# MOD-3.E  

# MOD-3.E.1  

Call Object class methods through inheritance.  

The Object class is the superclass of all other classes in Java.  

# MOD-3.E.2  

The Object class is part of the java.lang package  

# MOD-3.E.3  

The following Object class methods and constructors—including what they do and when they are used—are part of the Java Quick Reference:  

■ boolean equals(Object other) String toString()  

# MOD-3.E.4  

Subclasses of Object often override the equals and toString methods with classspecific implementations.  

# AP COMPUTER SCIENCE A  

# UNIT 10 Recursion  

Remember to go to AP Classroom to assign students the online Personal Progress Check for this unit.  

Whether assigned as homework or completed in class, the Personal Progress Check provides each student with immediate feedback related to this unit’s topics and skills.  

# Personal Progress Check 10  

# Multiple-choice: \~10 questions Free-response: 1 question  

$\cdot$ Methods and Control Structures (recursive and non-recursive solutions allowed)  

![](images/510bf9d2d2ceca0a05a973f5eb46bb46452649ccdb6f7c572621eb85aa9e3e6c.jpg)  

<html><body><table><tr><td>5-7.5 % APEXAMWEIGHTING</td><td>~3-5 CLASSPERIODS</td></tr></table></body></html>  

# Recursion  

# Developing Understanding  

# BIG IDEA 1  

# Control CON  

$-$ What real-world processes do you follow that are recursive in nature? Why do programmers sometimes prefer using recursive solutions when sorting data in a large data set?  

Sometimes a problem can be solved by solving smaller or simpler versions of the same problem rather than attempting an iterative solution. This is called recursion, and it is a powerful math and computer science idea. In this unit, students will revisit how control is passed when methods are called, which is necessary knowledge when working with recursion. Tracing skills introduced in Unit 2 are helpful for determining the purpose or output of a recursive method. In this unit, students will learn how to write simple recursive methods and determine the purpose or output of a recursive method by tracing.  

# Building Computational Thinking Practices  

# 1.B 2.C  2.D  

To better understand how recursion works, students should spend time writing their own recursive methods. Often, this can be overwhelming for students. One way to scaffold this skill for students is to require them to write a portion of program code, such as the base case, that can be used to complete the recursive method.  

# Preparing for the AP Exam  

Students should be able to determine the result of recursive method calls. Tracing the series of calls is a useful way to glean what the recursive method is doing and how it is accomplishing its purpose. Recursive algorithms, such as sorting and searching algorithms, often produce a result much more quickly than iterative solutions. Students also need to understand how many times statements in a recursive solution execute based on given input values.  

Recursion is primarily assessed through the multiple-choice section of the exam. Students are often asked to determine the result of a specific call to a recursive method or to describe the behavior of a recursive method. A call to a recursive method is just like a call to a nonrecursive method. Because a method is an abstraction of a process that has a specific result for each varied input, using a specific input value provides an understanding of how the method functions for that input. By understanding several instances of the method call, students can abstract and generalize the method’s overall purpose or process.  

While students will not be required to write a recursive solution in the free-response section, recursive solutions are often a more straightforward way of writing the solutions than iterative designs. Writing recursive solutions and analyzing calls to recursive methods help engage students with all aspects of recursive methods and provide them with a deeper understanding of how recursion works.  

![](images/4fff2e3d246d2411365ced05c59601d9173892ef5981c5c9c5ac258f5036a191.jpg)  

# Recursion  

# UNIT AT A GLANCE  

<html><body><table><tr><td>Enduring</td><td colspan="2">Topic Suggested Skills</td><td>Class Periods</td></tr><tr><td rowspan="4">CON-2</td><td>10.1 Recursion</td><td>1.BDetermine code thatwouldbe used to completecodesegments. 5.ADescribe the behavior of a given segment of</td><td>~3-5 CLASS PERIODS</td></tr><tr><td>10.2 Recursive Searching and Sorting</td><td>program code. 2.0Determine the result or output based on the statementexecutionorderinacodesegment</td><td></td></tr><tr><td></td><td>containing method calls. 2.DDetermine thenumberof timesa code segmentwillexecute.</td><td></td></tr><tr><td></td><td></td><td></td></tr><tr><td>AP</td><td colspan="2">Go to AP Classroom to assign the Personal Progress Check for Unit 10. Review the results in class to identify and address any student misunderstandings.</td><td></td></tr></table></body></html>  

# SAMPLE INSTRUCTIONAL ACTIVITIES  

The sample activities on this page are optional and are offered to provide possible ways to incorporate instructional approaches into the classroom. They were developed in partnership with teachers from the AP community to share ways that they approach teaching some of the topics in this unit. Please refer to the Instructional Approaches section beginning on p. 159 for more examples of activities and strategies.  

<html><body><table><tr><td>Activity</td><td>Topic</td><td>Sample Activity</td></tr><tr><td>1</td><td>10.1</td><td>Sharingandresponding Providestudentswiththepseudocodetomultiplerecursivealgorithms,andhave</td></tr><tr><td></td><td></td><td>studentswritethebasecaseoftherecursivemethodsandshareitwiththeirpartner. Thepartnershouldthenprovidefeedback,includinganycorrectionsoradditionsthat</td></tr><tr><td></td><td></td><td>may be needed.</td></tr><tr><td>2</td><td>10.1</td><td>Look for a pattern</td></tr><tr><td></td><td></td><td>Providestudentswitharecursivemethodandseveraldifferentinputs.Havestudents</td></tr><tr><td></td><td></td><td></td></tr><tr><td></td><td></td><td>runtherecursivemethod,recordthevariousoutputs,andlookforapatternbetween</td></tr><tr><td></td><td></td><td>theinputandrelatedoutput.Askstudentstowriteoneortwosentencesasabroad</td></tr><tr><td></td><td></td><td>descriptionofwhattherecursivemethod isdoing.</td></tr><tr><td></td><td></td><td></td></tr><tr><td>3</td><td>10.2</td><td>Code tracing</td></tr><tr><td></td><td></td><td>Whenlookingatarecursivemethod todeterminehowmanytimesitexecutes,have</td></tr><tr><td></td><td></td><td></td></tr><tr><td></td><td></td><td>studentscreateacalltreeorastacktracetoshowthemethodbeingcalledandthe</td></tr><tr><td></td><td></td><td>valuesofanyparametersofeachcall.Studentscanthencountupthenumberof</td></tr></table></body></html>  

![](images/835f50f2f1d70519249edae7b098f412d08781c804ab7e6649fe790f218db295.jpg)  

# Unit Planning Notes  

Use the space below to plan your approach to the unit. Consider how you want to pace your course and where you will incorporate analysis of recursive program code.  

# SUGGESTED SKILLS  

Determine code that would be used to complete code segments.  

# 5.A  

Describe the behavior of a given segment of program code.  

![](images/7d7c859fb7660e00818e6d8dcee77995692d686bbfac42ccf9c174b6b947465d.jpg)  

# AVAILABLE RESOURCES  

· Runestone Academy: AP CSA—Java Review: 12—Recursion   
Practice-It!: BJP4 Chapter 12: Recursion—SelfCheck 12.3–12.6, 12.13–12.15   
· CodingBat Java: Recursion  

# Recursion  

# TOPIC 10.1 Recursion  

# Required Course Content  

# ENDURING UNDERSTANDING  

# CON-2  

Programmers incorporate iteration and selection into code as a way of providing instructions for the computer to process each of the many possible input values.  

# LEARNING OBJECTIVE  

# ESSENTIAL KNOWLEDGE  

# CON-2.O  

# CON-2.O.1  

Determine the result of executing recursive methods.  

A recursive method is a method that calls itself.  

# CON-2.O.2  

Recursive methods contain at least one base case, which halts the recursion, and at least one recursive call.  

# CON-2.O.3  

Each recursive call has its own set of local variables, including the formal parameters.  

# CON-2.O.4  

Parameter values capture the progress of a recursive process, much like loop control variable values capture the progress of a loop.  

# CON-2.O.5  

Any recursive solution can be replicated through the use of an iterative approach.  

# EXCLUSION STATEMENT-(EK CON-2.O.5):  

Writing recursive program code is outside the scope of the course and AP Exam.  

# CON-2.O.6  

Recursion can be used to traverse String, array, and ArrayList objects.  

# SUGGESTED SKILLS  

# TOPIC 10.2 Recursive Searching and Sorting  

# 2.C  

Determine the result or output based on the statement execution order in a code segment containing method calls.  

Determine the number of times a code segment will execute.  

Required Course Content  

# ENDURING UNDERSTANDING  

# CON-2  

Programmers incorporate iteration and selection into code as a way of providing instructions for the computer to process each of the many possible input values.  

# LEARNING OBJECTIVE ESSENTIAL KNOWLEDGE  

# AVAILABLE RESOURCES  

§ Runestone Academy: AP CSA—Java Review: 13.3—Binary Search   
Runestone Academy: AP CSA—Java Review: 13.6—Merge Sort   
Practice-It!:BJP4 Chapter 12: Recursion—Exercises 12.1–12.3, 12.6–12.14, 12.18–12.22   
§ Practice-It!: BJP4 Chapter 13: Searching and Sorting—SelfCheck 12.30  

# CON-2.P  

Apply recursive search algorithms to information in String, 1D array, or ArrayList objects.  

# CON-2.P.1  

Data must be in sorted order to use the binary search algorithm.  

# CON-2.P.2  

The binary search algorithm starts at the middle of a sorted array or ArrayList and eliminates half of the array or ArrayList in each iteration until the desired value is found or all elements have been eliminated.  

# CON-2.P.3  

Binary search can be more efficient than sequential/linear search.  

# EXCLUSION STATEMENT—-(EK CON-2.P.3):  

Search algorithms other than sequential/linear and binary search are outside the scope of the course and AP Exam.  

# CON-2.P.4  

The binary search algorithm can be written either iteratively or recursively.  

# CON-2.Q  

Apply recursive algorithms to sort elements of array or ArrayList objects.  

# CON-2.Q.1  

Merge sort is a recursive sorting algorithm that can be used to sort elements in an array or ArrayList.  

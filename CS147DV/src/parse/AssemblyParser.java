package parse;
import java.util.Scanner;

/**
 * 
 * @author Jordan
 *
 *	A static class that can parse CS147DV instructions into their hexadecimal value
 */
public class AssemblyParser
{	
	/**
	 * Begins a console session where the user can input valid CS147DV commands and get the hex value in return.
	 * Console can be quit by typing quit or null
	 */
	public static void startConsoleParser()
	{
		System.out.println("Starting console");
		System.out.println("To see an example, enter help");
		Scanner input = new Scanner(System.in);
		String instruction = "";
		
		while(!instruction.equals("quit") && !instruction.equals("null"))
		{
			System.out.print("->");
			instruction = input.nextLine();
			
			try 
			{
				if(instruction.toLowerCase().trim().equals("help"))
				{
					System.out.println("\nExample syntax for addi register 1, register 2, 0x10 (note that this value must be converted to decimal):");
					System.out.println("-> addi r1, r2, 16");
					System.out.println(parse("addi r1, r2, 16") + "\n");
				}
				else if(!instruction.equals("quit") && !instruction.equals("null") )
					System.out.println(parse(instruction));
				
			}
			catch(RuntimeException e)
			{
				System.out.println("An Error has occured. Ensure that your instruction is valid and try again");
			}
		}
		
		System.out.println("Closing the console");
		input.close();
	}
	
	/**
	 * Parses a valid CS147DV instruction and returns the instruction in hexadecimal
	 * @param cs147dvInstruction a valid CS147DV instruction
	 * @return the hexadecimal value of the instruction
	 */
	public static String parse(String cs147dvInstruction)
	{
		//default values
		String opcode = "000000";
		String rd = "00000"; 
		String rs = "00000"; 
		String rt = "00000"; 
		String shamt = "00000";
		String funct = "000000";
		String imm = "0000000000000000";
		String addr = "00000000000000000000000000";
		
		String[] instruction = cs147dvInstruction.trim().split("\\s+");
		
		opcode = toNBitString(mnemonicToOpcode(instruction[0]), 6);
		
		switch(mnemonicToOpcode(instruction[0]))
		{
			case 0x00:	{ // R-type instructions
						
							if(mnemonicToFunct(instruction[0]) == 0x08) //jump register
							{
								rs = parseRegister(instruction[1]);
							}
							else 
							{
								rd = parseRegister(instruction[1]);
								rs = parseRegister(instruction[2]);
								
								if(mnemonicToFunct(instruction[0]) == 0x01 || mnemonicToFunct(instruction[0]) == 0x02) //shift
								{
									shamt = toNBitString(Integer.parseInt(instruction[3]), 5);
								}
								else //all other r type instructions
								{
									rt =  parseRegister(instruction[3]);
								}
							}
							funct = toNBitString( mnemonicToFunct(instruction[0]), 6);
							
							String binResult = opcode + rs + rt + rd + shamt + funct;
							int parsedBinResult = Integer.parseInt(binResult, 2);
							return padWithZeros(Integer.toHexString(parsedBinResult), 8);
						}
			
			case 0x08: case 0x1d: case 0x0c: case 0x0d: 
			case 0x0a: case 0x04: case 0x05: case 0x23:
			case 0x2b:	{ // All I-type instructions except load upper immediate
							rt = parseRegister(instruction[1]);
							rs = parseRegister(instruction[2]);
							imm = toSignedNBitString(Integer.parseInt(instruction[3]), 16);
							
							String binResult = opcode + rs + rt + imm;
							int parsedBinResult = Integer.parseUnsignedInt(binResult, 2);
							return padWithZeros(Integer.toHexString(parsedBinResult), 8);
						}
			case 0x0f:	{ //load upper immediate
							rt = parseRegister(instruction[1]);
							imm = toSignedNBitString(Integer.parseInt(instruction[2]), 16);
							
							String binResult = opcode + rs + rt + imm;
							int parsedBinResult = Integer.parseInt(binResult, 2);
							return padWithZeros(Integer.toHexString(parsedBinResult), 8);
						}
			
			case 0x02: //jump
			case 0x03:	{ //jump and link
							addr = toNBitString(Integer.parseInt(instruction[1]), 26);
							
							String binResult = opcode + addr;
							int parsedBinResult = Integer.parseInt(binResult, 2);
							return padWithZeros(Integer.toHexString(parsedBinResult), 8);
						}
			case 0x1b: //push
			case 0x1c:	{ //pop
							String binResult = opcode + addr;
							int parsedBinResult = Integer.parseInt(binResult, 2);
							return padWithZeros(Integer.toHexString(parsedBinResult), 8);
						}
			
			default : return "00000000";
		}		
	}
	
	/**
	 * Gets the funct of an R-type instruction in CS147DV
	 * @param mnemonic the mnemonic of the instruction
	 * @return the funct
	 */
	private static int mnemonicToFunct(String mnemonic)
	{
		switch(mnemonic.toLowerCase())
		{
			case "add" : return 0x20;
			case "sub" : return 0x22;
			case "mul" : return 0x2c;
			case "and" : return 0x24;
			case "or"  : return 0x25;
			case "nor" : return 0x27;
			case "slt" : return 0x2a;
			case "sll" : return 0x01;
			case "srl" : return 0x02;
			case "jr" : return 0x08;
			
			default : return 0x0;
		}
	}
	
	/**
	 * Gets the opcode of an instruction in CS147DV
	 * @param mnemonic the mnemonic of the instruction
	 * @return the opcode
	 */
	private static int mnemonicToOpcode(String mnemonic)
	{
		switch(mnemonic.toLowerCase())
		{
			//I type instructions
			case "addi" : return 0x08;
			case "muli" : return 0x1d;
			case "andi" : return 0x0c;
			case "ori" : return 0x0d;
			case "lui" : return 0x0f;
			case "slti" : return 0x0a;
			case "beq" : return 0x04;
			case "bne" : return 0x05;
			case "lw" : return 0x23;
			case "sw" : return 0x2b;
			
			//J type instructions
			case "jmp" : return 0x02;
			case "jal" : return 0x03;
			case "push" : return 0x1b;
			case "pop" : return 0x1c;
			
			//R type instructions
			default : return 0x00;
		}
	}
	
	/**
	 * Returns a 5 bit unsigned binary value based on the address of the register passed in
	 * @param register a string representing a register with the format r# or r#,
	 * @return
	 */
	private static String parseRegister(String register)
	{
		int regAddress = Integer.parseInt(register.substring(1).replace(",", "")); // regNumber is the address of the register, which is between 0 and 31
		
		return toNBitString(regAddress, 5);
	}
	
	/**
	 * Converts an integer into an unsigned binary string of size n
	 * @param input the integer to convert
	 * @param n the final size of the string
	 * @return an n bit unsigned binary number represented by a String
	 */
	private static String toNBitString(int input, int n)
	{
		String zeros = "";
		
		for(int i = 0; i < n; i++)
			zeros = zeros + "0";
		
		String binaryString = Integer.toBinaryString(input);
		
		
		return padWithZeros(binaryString, n);
	}
	
	/**
	 * Prepends the input string with 0s until the maximum size n is reached
	 * @param input the string to pad
	 * @param n the final size of the string
	 * @return the string appended with 0s
	 */	
	private static String padWithZeros(String input, int n)
	{
		String zeros = "";
		
		for(int i = 0; i < n; i++)
			zeros = zeros + "0";
		
		String formatted = (zeros + input).substring(input.length()); 
		return formatted;
	}
	
	/**
	 * Takes a signed integer/immediate value and sign extends it up to n digits in binary
	 * @param input a signed immediate value
	 * @param n the size to extend the value to
	 * @return a string representing the sign extended integer in binary
	 */
	private static String toSignedNBitString(int input, int n)
	{
		String msb;
		if(input <0)
			msb = "1";
		else 
			msb = "0";
		
		String binaryString = Integer.toBinaryString(input);

		String extend = "";
		
		for(int i = 0; i < n; i++)
			extend = extend + msb;
		
		String formatted = (extend + binaryString).substring(binaryString.length()); 
		
		return formatted;
	}

}

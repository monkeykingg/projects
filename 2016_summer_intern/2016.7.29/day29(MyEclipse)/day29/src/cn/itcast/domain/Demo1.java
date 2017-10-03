package cn.itcast.domain;

import java.math.BigDecimal;

public class Demo1 {

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		
		/*double a = 0.1;
		double b = 0.006;
		
		System.out.println(a+b);*/
		
		BigDecimal a = new BigDecimal("0.1");
		BigDecimal b = new BigDecimal("0.006");
		
		System.out.println(a.add(b).toString());
		System.out.println(a.multiply(b).toString());
		System.out.println(a.divide(b,10,BigDecimal.ROUND_HALF_UP).toString());

	}

}

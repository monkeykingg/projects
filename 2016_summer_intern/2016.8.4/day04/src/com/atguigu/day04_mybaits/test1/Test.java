package com.atguigu.day04_mybaits.test1;

import java.io.IOException;
import java.io.InputStream;

import org.apache.ibatis.session.SqlSession;
import org.apache.ibatis.session.SqlSessionFactory;
import org.apache.ibatis.session.SqlSessionFactoryBuilder;

public class Test {
	
	public static void main(String[] args) throws IOException{
		
		String resource = "conf.xml";
		
		InputStream is = Test.class.getClassLoader().getResourceAsStream(resource);
		
		SqlSessionFactory factory = new SqlSessionFactoryBuilder().build(is);
		
		SqlSession session = factory.openSession();
		
		String statement = "com.atguigu.day04_mybaits.test1.userMapper.getUser";
		User user = session.selectOne(statement, 2);
		
		System.out.println(user);
	}
	
}

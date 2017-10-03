package junit.test;

import java.util.Date;

import org.junit.Test;

import cn.itcast.dao.imp1.UserDaoImp1;
import cn.itcast.domain.User;

public class UserDaoTest {
	
	@Test
	public void testAdd(){
		User user = new User();
		user.setBirthday(new Date());
		user.setEmail("test@outlook.com");
		user.setId("123456789");
		user.setNickname("Tester");
		user.setPassword("987654321");
		user.setUsername("test");
		
		UserDaoImp1 dao = new UserDaoImp1();
		dao.add(user);
	}

}

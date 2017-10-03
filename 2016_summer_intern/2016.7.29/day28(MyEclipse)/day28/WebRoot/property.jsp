<%@ page language="java" import="java.util.*" pageEncoding="UTF-8"%>

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
  <head>
    
    <title>JSP: setProperty标签应用</title>

  </head>
  
  <body>
    
    <jsp:useBean id="person" class="cn.itcast.domain.Person"></jsp:useBean>
    
    <!-- 手工为bean属性赋值  -->
    <jsp:setProperty property="name" name="person" value="Property_changed"/>  
    <%=person.getName() %><br/>
    
    
    <!-- 用请求参数为bean属性赋值 例：http://localhost:8080/day28/property.jsp?name=wwwwwwwww-->
    <jsp:setProperty property="name" name="person" param="name"/>
    
    <!-- 例：http://localhost:8080/day28/property.jsp?name=wwwwww&age=18-->
    <jsp:setProperty property="age" name="person" param="age"/> <!-- 支持八种基本数据类型转换（把客户机提交的字符串，转换成相应的八种基本类型，赋到bean的属性上） -->
    
    <!-- 例：http://localhost:8080/day28/property.jsp?name=wwwwww&age=18 -->
    <jsp:setProperty property="birthday" name="person" value="<%=new Date() %>"/>
    
    
    <%=person.getName() %><br/>
    <%=person.getAge() %><br/>
    <%=person.getBirthday() %><br/>
    
    
    <br/>=================================<br/>
    
    
    <!-- 用所有的请求参数为bean赋值 -->
    <jsp:setProperty property="*" name="person"/>
    <%=person.getName() %><br/>
    <%=person.getAge() %><br/>
    
    
    <jsp:getProperty property="name" name="person"/>
    <jsp:getProperty property="age" name="person"/>
    <jsp:getProperty property="birthday" name="person"/>
    
  </body>
</html>

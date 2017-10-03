<%@ page language="java" import="java.util.*" pageEncoding="UTF-8"%>
<%@ page import="cn.itcast.domain.Person" %>
<%@ page import="cn.itcast.domain.Address" %>

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
  <head>
    
    <title>EL</title>

  </head>
  
  <body>
    
    
    
    <%
    	String data = "bilibili";
    	request.setAttribute("data", data); 
     %>
    ${data }  <%-- 相当于pageContext.findAttribute("data") "page"-"request"-"session"-"application" --%>
    
    
    
    
    
    <br/>
    <%
     	Person p = new Person();
    	p.setName("Ace");
    	request.setAttribute("person", p); 
     %>
     ${person.name }  <%-- 相当于pageContext.findAttribute("person") "page"-"request"-"session"-"application" --%>
    
    
    
    
    <br/>
    <%
    	Person p1 = new Person();
    	Address a = new Address();
    	a.setCity("Toronto");
    	p1.setAddress(a);
    	
    	request.setAttribute("p1", p1);
     %>
     ${p1.address.city }
     
     
     
     
     
     <br/>
     <%
     	List list = new ArrayList();
     	list.add(new Person("Ace"));
     	list.add(new Person("Bill"));
     	list.add(new Person("David"));
     	
     	request.setAttribute("list", list);
      %>
      ${list[1].name }
    
    
    
    
    <br/>
    <%
    	Map map = new HashMap();
    	map.put("David", new Person("David"));
    	map.put("Bill", new Person("Bill"));
    	map.put("Ace", new Person("Ace"));
    	request.setAttribute("map", map);
     %>
    ${map.David.name }
    
    
    <br/>
    ${pageContext.request.contextPath }
    
    <br/>
    <a href="${pageContext.request.contextPath }/index.jsp">点击链接</a>
    
  </body>
</html>

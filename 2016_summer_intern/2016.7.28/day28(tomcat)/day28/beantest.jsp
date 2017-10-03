<%@ page language="java" import="java.util.*" pageEncoding="UTF-8"%>

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
  <head>
    
    <title>JSP: usebean标签应用</title>

  </head>
  
  <body>
    <!-- usebean标签的标签只在usebean标签实例化bean时才执行  -->
    <jsp:useBean id="person" class="cn.itcast.domain.Person" scope="page">
    	TESTTESTTESTTEST
    </jsp:useBean>
    
    <%=person.getName() %>
    
  </body>
</html>

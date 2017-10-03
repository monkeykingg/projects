<%@ page language="java" import="java.util.*" pageEncoding="UTF-8"%>

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
  <head>
  
    <title>动态包含（运行时包含）</title>
    
  </head>
  
  <body>
    	
	<%
	
		request.getRequestDispatcher("/public/head.jsp").include(request, response);
	
	%>


	<%
	
		response.getWriter().write("TEST<br/>");
	
	 %>


	<%
	
		request.getRequestDispatcher("/public/foot.jsp").include(request, response);
	
	%>

  </body>
</html>

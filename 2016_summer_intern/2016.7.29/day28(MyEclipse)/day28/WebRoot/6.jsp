<%@ page language="java" import="java.util.*" pageEncoding="UTF-8"%>

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
  <head>
  
    <title>JSP include 指令（静态包含，编译时包含）</title>
    
  </head>
  
  <body>
    	
	<%@include file="/public/head.jsp" %>

	TEST<br/>

	<%@include file="/public/foot.jsp" %>

  </body>
</html>

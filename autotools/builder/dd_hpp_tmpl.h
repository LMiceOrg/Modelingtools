﻿$def with (ctx)
/******************************************************************************************************************************
 定义什么代表字符串的空值	    "" 字符串没有值
	定义double类型变量的无效值      //IEEE754  double, float : NAN作为无效值
	定义long类型变量的无效值        LONG_MAX 作为无效值
	
	#define infinum			(1.0e38)//
	#define  PI 3.14159265358979323846
	#define NearlyZero		(1.0e-7)
	#define FI				(57.29578)//弧度到度的转换系数
	#define toRad           (PI/180)//度到弧度的转换系数
	#define LawsNearlyZero	(1.0e-4)
	#define  Re 6371000.0	//地球半径
	#define  Go = 9.81
	#define SMALL 1e-6
******************************************************************************************************************************/

#ifndef NTSIM_Data_Define_Include_H
#define NTSIM_Data_Define_Include_H

#include <limits.h>

//定义字符串的空值
#define NTSTRING_EMPTY 	""

//定义double类型变量的无效值 
#define NTDOUBLE_EMPTY 	NAN

//定义double类型的无穷大
#define NTDOUBLE_INF 	INFINITY

//定义long类型变量的无效值
#define NTLONG_EMPTY 	LONG_MAX

//地球半径
#define  NT_Re 			6371393.0

//加速度
#define  NT_Go 			9.81

//圆周率
#if defined(M_PI)
#define NT_PI 			M_PI
#else
#define  NT_PI 			3.14159265358979323846
#endif

//度到弧度的转换系数
#define NT_TORAD   		0.017453292519943295

//弧度到度的转换系数
#define NT_FI			57.29577951308232

#endif //NTSIM_Data_Define_Include_H

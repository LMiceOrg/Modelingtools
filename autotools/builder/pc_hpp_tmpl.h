$def with (ctx)
/****************************************************************************
**
**  开发单位：$ctx['user_dept']
**  开发者：$ctx['user_name']
**  创建时间：$ctx['tm_now']
$if ctx.has_key('version'):
    **  版本号：$ctx['version']
$else:
    **  版本号：V1.0
$if ctx.has_key('h_name'):
    **  描述信息：$ctx['h_name']
$else:
    **  描述信息：$ctx['H_NAME']
**  返回值: true: means the  parameter in within reasonable extent
           false: means the  parameter in unreasonable
****************************************************************************/


#ifndef NTSIM_Parameter_Checker_Include_H
#define NTSIM_Parameter_Checker_Include_H


#include <string>
#include <stdlib.h>
#include <ctype.h>
using namespace std;


/****Method to check int type  parameter****************************************/
static inline bool int_parameter_checker( int parameter, const int minimum, const long maximum )
{
	if ( ( parameter < minimum ) || ( parameter > maximum ) )
	{
		return false;                                             // parameter is unreasonable 
	}
	else
	{
		return true;                                              // parameter is reasonable
	}

}

/****Method to check float type  parameter****************************************/
static inline bool float_parameter_checker ( float parameter, const double minimum, const double maximum )
{
	if ( ( parameter < minimum ) || ( parameter > maximum ) )
	{
		return false;                                             // parameter is unreasonable 
	}
	else
	{
		return true;                                              // parameter is reasonable
	}

}

/****Method to check float type  parameter****************************************/
static inline bool float_parameter_checker_1 ( float parameter, const double minimum, const double maximum )
{
	if ( ( parameter <= minimum ) || ( parameter > maximum ) )
	{
		return false;                                             // parameter is unreasonable 
	}
	else
	{
		return true;                                              // parameter is reasonable
	}

}

/****Method to check double type  parameter****************************************/
static inline bool double_parameter_checker ( double parameter, const double minimum, const double maximum )
{
	if ( ( parameter < minimum ) || ( parameter > maximum ) )
	{
		return false;                                             // parameter is unreasonable 
	}
	else
	{
		return true;                                              // parameter is reasonable
	}

}

static inline bool LON_Checker(double parameter)
{
	return double_parameter_checker(parameter, -180, 180);
}

static inline bool LAT_Checker(double parameter)
{
	return double_parameter_checker(parameter,-90,90);
}

static inline bool Height_Checker(float parameter)
{
	return float_parameter_checker(parameter,0,50000);
}


static inline bool AZ_Checker(float parameter)
{
	return float_parameter_checker(parameter,0,360);
}

static inline bool EL_Checker(float parameter)
{
	return float_parameter_checker(parameter,-90,90);
}


/****Method to check long type  parameter****************************************/
static inline bool long_parameter_checker ( long parameter, const long minimum, const long maximum )
{
	if ( ( parameter < minimum ) || ( parameter > maximum ) )
	{
		return false;                                             // parameter is unreasonable 
	}
	else
	{
		return true;                                              // parameter is reasonable
	}

} 

/****Method to check short type  parameter****************************************/
static inline bool short_parameter_checker ( short parameter, const short minimum, const long maximum ) 
{
	if ( ( parameter < minimum ) || ( parameter > maximum ) )
	{
		return false;                                             // parameter is unreasonable 
	}
	else
	{
		return true;                                              // parameter is reasonable
	}

}

/****Method to check unsigned short type  parameter****************************************/
static inline bool unsignedshort_parameter_checker (unsigned short parameter, const unsigned short minimum, const unsigned short maximum ) 
{
	if ( ( parameter < minimum ) || ( parameter > maximum ) )
	{
		return false;                                             // parameter is unreasonable 
	}
	else
	{
		return true;                                              // parameter is reasonable
	}

}

/****Method to check unsigned long type  parameter****************************************/
static inline bool unsignedlong_parameter_checker ( unsigned long parameter, const unsigned long minimum, const unsigned long maximum )
{
	if ( ( parameter < minimum ) || ( parameter > maximum ) )
	{
		return false;                                             // parameter is unreasonable 
	}
	else
	{
		return true;                                              // parameter is reasonable
	}

}


/****Method to check enum type  parameter****************************************/
template <class T> bool enum_parameter_checker ( T parameter, const short minimum, const short maximum ) 
{
	if ( ( ( unsigned short )parameter < minimum ) || ( ( unsigned short )parameter > maximum ) )
	{
		return false;                                             // parameter is unreasonable 
	}
	else
	{
		return true;                                              // parameter is reasonable
	}	
}

/****Method to check double type  parameter only min ****************************************/
static inline bool doublemin_parameter_checker ( double parameter, const double minimum)
{
	if ( parameter < minimum )
	{
		return false;                                             // parameter is unreasonable 
	}
	else
	{
		return true;                                              // parameter is reasonable
	}
}

/****Method to check float type  parameter only min****************************************/
static inline bool floatmin_parameter_checker ( float parameter, const float minimum)
{
	if ( parameter <= minimum )
	{
		return false;                                             // parameter is unreasonable 
	}
	else
	{
		return true;                                              // parameter is reasonable
	}
}


enum RangeType
{
	RT_LEFT,
	RT_RIGHT,
	RT_MIDDLE
 };
enum EndType
{
	ET_OPEN,
	ET_CLOSE
};
/**
 * 值域描述结构
 * 名称： ValueRange
 * 作用： 用于对参数的取值范围进行描述
 * 属性：
 *      type： 范围类型描述
 *      left：  区间左端点开闭类型描述
 *      right： 区间右端点开闭类型描述
 * 操作：
 *      Check： 对输入参数进行合法性检查
 */
template<class T>
struct ValueRange
{
	RangeType type;
	EndType left,right;

	T min;
	T max;

	/**
	 * 构造函数
	 * 名称： ValueRange
	 * 作用： 初始化成员变量
	 * 参数：
	 *      
	 * 返回值：
	 *      
	 */
	ValueRange()
	{
		this->type = RT_MIDDLE;
		this->left = ET_CLOSE;
		this->right = ET_CLOSE;

		this->min = T(0);
		this->max = T(1);
	}
	/**
	 * 构造函数
	 * 名称： ValueRange
	 * 作用： 初始化成员变量
	 * 参数：
	 *      
	 * 返回值：
	 *      
	 */
	ValueRange(T min, T max, RangeType type = RT_MIDDLE, EndType left = ET_CLOSE, EndType right = ET_CLOSE)
	{
		this->type = type;
		this->left = left;
		this->right = right;

		this->min = min;
		this->max = max;
	}

	/**
	 * 参数检查函数
	 * 名称： Check
	 * 作用： 对输入参数进行合法性检查
	 * 参数：
	 *      v： 输入参数值
	 * 返回值：
	 *      bool型： 输入值合法性检查结果
	 */
	bool Check(T v)
	{
		bool valid = true;

		//对不同的值域类型分别进行检查
		switch(this->type)
		{
		case RT_MIDDLE:		//如果是大于小于类型
			{
				//左侧
				if(left == ET_CLOSE)
				{
					//左侧为闭区间
					valid = valid && ( !(v < min) );
				}
				else
				{
					//左侧为开区间
					valid = valid && (v > min);
				}

				//右侧
				if(right == ET_CLOSE)
				{
					//右侧为闭区间
					valid = valid && ( !(v > max) );
				}
				else
				{
					//右侧为开区间
					valid = valid && (v < max);
				}
			}
			break;
		case RT_LEFT:		//如果是小于类型
			{
				//只检测右侧
				if(right == ET_CLOSE)
				{
					//右侧为闭区间
					valid = valid && ( !(v > max) );
				}
				else
				{
					//右侧为开区间
					valid = valid && (v < max);
				}
			}
			break;
		case RT_RIGHT:		//如果是大于类型
			{
				//只检测左侧
				if(left == ET_CLOSE)
				{
					//左侧为闭区间
					valid = valid && ( !(v < min) );
				}
				else
				{
					//左侧为开区间
					valid = valid && (v > min);
				}
			}
			break;
		default:
			break;
		}
		return valid;
	}
};

/*
inline bool parameter_checker(int v,ValueRange<int> *pr) { return pr->Check(v); } 
inline bool parameter_checker(float v,ValueRange<float> *pr) { return float_parameter_checker(v,pr->min,pr->max); } 
inline bool parameter_checker(double v,ValueRange<double> *pr) { return double_parameter_checker(v,pr->min,pr->max); } 
inline bool parameter_checker(long v,ValueRange<long> *pr) { return long_parameter_checker(v,pr->min,pr->max); } 
inline bool parameter_checker(short v,ValueRange<short> *pr) { return short_parameter_checker(v,pr->min,pr->max); } 
inline bool parameter_checker(unsigned short v,ValueRange<unsigned short> *pr) { return unsignedshort_parameter_checker(v,pr->min,pr->max); } 
inline bool parameter_checker(unsigned long v,ValueRange<unsigned long> *pr) { return unsignedlong_parameter_checker(v,pr->min,pr->max); } 
inline bool parameter_checker(bool v) { return bool_parameter_checker(v); } 
template <class T> inline bool parameter_checker(T v,ValueRange<T> *pr) { return enum_parameter_checker(v,pr->min,pr->max); } 
*/

//bool型值域，因为bool型数值总是有效的，因此，并不需要真正进行检查，其值域
//范围也是不需要的，因此，此处定义一个空的bool型值域结构值，仅做占位处理
#define BOOLEANRANGE (*((ValueRange<bool> *)NULL))

/**
 * 参数检查函数模板
 * 名称： parameter_checker
 * 作用： 对输入参数进行合法性检查
 * 参数：
 *      v： 输入参数值
 *     pr： 值域描述
 * 返回值：
 *      bool型： 输入值合法性检查结果
 */
template <class T>
inline bool parameter_checker(T v,ValueRange<T> *pr)
{
	return pr->Check(v);
}
/**
 * bool型参数检查函数
 * 名称： parameter_checker
 * 作用： 对输入参数进行合法性检查
 * 参数：
 *      v： 输入参数值
 *     pr： 值域描述
 * 返回值：
 *      bool型： 输入值合法性检查结果
 */
inline bool parameter_checker(bool v,ValueRange<bool> *pr)
{
	return true;
}

#endif //NTSIM_Parameter_Checker_Include_H


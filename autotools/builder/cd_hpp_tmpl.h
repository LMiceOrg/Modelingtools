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
****************************************************************************/


#ifndef $ctx['H_NAME']_COMPDATA_H_
#define $ctx['H_NAME']_COMPDATA_H_

#include "$ctx['l_typedef']$'.h'"

/** 引用类型声明 */
$ctx['predeclare']

//namespace $ctx['h_name']
//{

/** 复合结构体类型 */
$ctx['structlist']

//} /* end of namespace $ctx['h_name'] */

/** LMice::is_pod 模版特化 */
namespace LMice {
//is_pod
}


#endif //$ctx['H_NAME']_COMPDATA__H_

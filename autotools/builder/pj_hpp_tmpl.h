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


#ifndef $ctx['H_NAME']_LOCAL_H_
#define $ctx['H_NAME']_LOCAL_H_

#include "$ctx['autotools'].l_ns_name.lower()_typedef.h"

#pragma pack(1)

#include "datadefine.h"

#include "parametercheck.h"

$if ctx.has_key('headers'):
    $for ns in ctx['headers']:
        #include "$ns.lower()$'.h'"

    $# endfor headers
$# endif headers

//有依赖顺序的结构体
#include "$ctx['autotools'].l_ns_name.lower()_depends.h"

//模型消息与事件结构体
#include "$ctx['autotools'].l_ns_name.lower()_model.h"

#pragma pack()

#endif //$ctx['H_NAME']_LOCAL_H_

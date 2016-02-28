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


#ifndef $ctx['H_NAME']_ENUMDATA_H_
#define $ctx['H_NAME']_ENUMDATA_H_

namespace $ctx['h_name']
{

/** 枚举类型 */
$ctx['enumlist']

} /* end of namespace $ctx['h_name'] */

#endif //$ctx['H_NAME']_ENUMDATA_H_

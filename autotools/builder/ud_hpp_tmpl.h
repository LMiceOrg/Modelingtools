$def with (ctx)

#ifndef $ctx['PJ_NAME']_USERDATATYPE_H_
#define $ctx['PJ_NAME']_USERDATATYPE_H_

#include <AppSimKernel.h>
using namespace AppSim;

// NTSim global type definition
#include "../../../common/include/$ctx['autotools'].l_ns_name.lower()$'.h'"
using namespace $ctx['autotools'].l_ns_name;

#include <map>
#include <string>
#include <vector>
using std::string;
using std::vector;
using std::map;


//实现类类型预先声明
class C$ctx['pj_name']Impl;


// 在接口类添加实现类的成员变量
//friend class C$ctx['pj_name']Impl;
//C$ctx['pj_name']Impl* pmodel;

#endif /** $ctx['PJ_NAME']_USERDATATYPE_H_ */

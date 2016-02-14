$def with(ctx)
#ifndef $ctx['PJ_NAME']_EXPORT_H_
#define $ctx['PJ_NAME']_EXPORT_H_
#if defined(_WIN32)
        #pragma warning(disable: 4251)
        #if defined($ctx['PJ_NAME']_EXPORTS)
                #define $ctx['PJ_NAME']_API __declspec(dllexport)
        #else
                #define $ctx['PJ_NAME']_API __declspec(dllimport)
        #endif
#else
        #define $ctx['PJ_NAME']_API
#endif

#endif /** $ctx['PJ_NAME']_EXPORT_H_ */

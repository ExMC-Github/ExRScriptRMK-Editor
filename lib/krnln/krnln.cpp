#include <windows.h>
#include <string>
#include <shlwapi.h>
using std::wstring;
#pragma comment(lib, "shlwapi.lib")

// 全局变量保存DLL路径
wstring g_dllLoadPath;

// 从krnln.fnr导入GetNewSock函数
typedef int (*GETNEWSOCK_FUNC)(int);
GETNEWSOCK_FUNC pGetNewSock = nullptr;

BOOL APIENTRY DllMain(HMODULE hModule, DWORD dwReason, LPVOID lpReserved)
{
    if (dwReason == DLL_PROCESS_ATTACH)
    {
        // 获取当前DLL所在目录
        wchar_t modulePath[MAX_PATH];
        GetModuleFileNameW(hModule, modulePath, MAX_PATH);
        PathRemoveFileSpecW(modulePath);
        
        // 创建lib目录
        g_dllLoadPath = wstring(modulePath) + L"\\lib";
        CreateDirectoryW(g_dllLoadPath.c_str(), NULL);
        
        // 设置DLL加载目录
        SetDllDirectoryW(g_dllLoadPath.c_str());
        
        // 构建krnln.fnr的完整路径
        wstring krnlnPath = g_dllLoadPath + L"\\krnln.fnr";
        
        // 从lib目录加载krnln.fnr并获取函数地址
        HMODULE hKrnln = LoadLibraryW(krnlnPath.c_str());
        if (hKrnln)
        {
            pGetNewSock = (GETNEWSOCK_FUNC)GetProcAddress(hKrnln, "GetNewSock");
        }
        else
        {
            // 如果加载失败，可以输出错误信息（调试时使用）
            // 在实际发布版本中可能需要移除或记录到日志
            DWORD error = GetLastError();
            // 可以在这里添加错误处理代码
        }
        
        // 禁用线程库调用（可选，提高性能）
        DisableThreadLibraryCalls(hModule);
    }
    else if (dwReason == DLL_PROCESS_DETACH)
    {
        // 清理工作
        if (pGetNewSock)
        {
            // 如果需要在卸载时清理，可以在这里处理
        }
    }
    return TRUE;
}

// 导出函数
extern "C" __declspec(dllexport) int GetNewSock(int arg1)
{
    if (pGetNewSock)
    {
        return pGetNewSock(arg1);
    }
    return 0; // 如果函数未加载成功，返回0或其他错误值
}

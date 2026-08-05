# 17 — Deploying This Repo (Execution Guide)

Everything below is scripted and ready to run — this doc is the order to
run it in.

## 1. Provision the VMs
```bash
vagrant up manager
vagrant up linux_victim
# windows_victim: replace the placeholder box in Vagrantfile first, see 02-victim-vm-setup.md
vagrant up windows_victim
```
Or provision manually following [01](01-environment-setup.md) /
[02](02-victim-vm-setup.md) if not using Vagrant.

`install/install-wazuh-manager.sh` and `install/setup-linux-victim.sh` are
also wired in as Vagrant provisioners, so a plain `vagrant up` does the
software install automatically — no separate step needed if using Vagrant.

## 2. If not using Vagrant, run the install scripts directly
```bash
# On the manager:
sudo ./install/install-wazuh-manager.sh

# On the Linux victim:
sudo ./install/setup-linux-victim.sh 192.168.56.10

# On the Windows victim (as Administrator):
.\install\setup-windows-victim.ps1 -ManagerIp 192.168.56.10
```

## 3. Confirm agents are connected
Wazuh Dashboard → Agents → both victims should show **Active**.

## 4. Run the atomics
```powershell
# Windows victim
.\scripts\run-atomics.ps1
```
```bash
# From a third "attacker" VM on the same host-only network
./scripts/run-brute-force.sh 192.168.56.21
```

## 5. Watch the dashboard
Filter alerts by `rule.id: 100010-100060` (this lab's custom rule ID
range) or search for `mitre.id` matching the technique being tested.

## 6. Record results
Update the matching `results/<ID>-results.md` with what actually happened
— including partial/negative results, following the pattern already in
this repo. Don't round a partial pass up to a full one.

## 7. Clean up
```powershell
.\scripts\run-atomics.ps1 -Cleanup
```
```bash
vagrant destroy -f
```
